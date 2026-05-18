"""
grid_library — grid editorial mensal por marca (InsideOut).

Terceiro pilar da geração de social media (os outros dois: `style_library`
= "como a peça parece"; `product_library` = "o que é o produto e como a marca
fala"). Aqui mora **"o que postar e quando"**: um grid = 1 marca × 1 mês, com
o esqueleto semanal que a Estela (social media Clinique/EL/TF) usa hoje em
duas planilhas Excel — colapsadas num único artefato canônico.

Princípios (mesmos do `product_library`, ver plano merry-snacking-flame):
- Dados na PASTA DE TRABALHO do usuário — 1 JSON por grid
  (`<workspace>/grids/<marca>/<AAAA-MM>.json`). Nunca no plugin dir.
- O grid HTML é SEMPRE derivado (gerado do JSON) — nunca fonte de dado, nunca
  editado por string (a planilha apodrecia exatamente por edição à mão).
- Escrita atômica; delete é soft (.trash/); nada de "apagar tudo".
- Sem workspace, cai no seed embarcado (read-only) — zero-config funciona.
- **Regras da Estela** vivem em `grids/rules/<marca>.md` (Markdown editável
  por humano, não hardcoded) e o **calendário comemorativo** em
  `grids/calendar/<ano>.md` (compartilhado entre marcas). Consumidos na Fase 2
  (`generate_from_briefing`); a Fase 1 só os materializa do seed.

A disciplina UWP-safe (nunca `.resolve()` em `__file__` de plugin; desconfiar
de todo stat do plugin dir) vive em `_libcommon`. Sem efeitos colaterais no
import.
"""
from __future__ import annotations

import calendar
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import _libcommon as lc

SCHEMA_VERSION = 1
LIB_DIRNAME = "grids"
ENV_OVERRIDE = "GRIDS_DIR"

_CORE_DIR = lc.CORE_DIR
_SEED_FILE = _CORE_DIR / "grids.seed.json"
_RULES_SEED_DIR = _CORE_DIR / "rules-seed"
_CALENDAR_SEED_DIR = _CORE_DIR / "calendar-seed"
_TEMPLATE_FILE = _CORE_DIR / "grid-template.html"
_PLACEHOLDER = "/*__GRID_JSON__*/null"

# Subdirs reservados dentro de grids/ — NÃO são marcas.
_RESERVED = {"rules", "calendar", "mockups", ".trash"}

# Abreviação PT do dia da semana, indexada com domingo=0 (a planilha da Estela
# é DOMINGO..SÁBADO).
_DOW = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"]

_PT_MONTHS = {
    "janeiro": 1, "fevereiro": 2, "marco": 3, "março": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8, "setembro": 9,
    "outubro": 10, "novembro": 11, "dezembro": 12,
}

# Escopo de ingestão travado com o Lucas (2026-05-18): só 2026 já valida o
# modelo de dados; histórico 2025 fica fora.
INGEST_YEAR = 2026

# Campos de um "dia" do grid que as operações de post podem mover/editar
# (data e dow são identidade do slot, não conteúdo).
_POST_FIELDS = ("channel", "approach", "product", "subject", "ref",
                "lettering", "mockup", "rationale", "notes")


class GridError(lc.LibCommonError):
    """Erro base do grid."""


class GridNotFound(GridError):
    pass


class InvalidGrid(GridError):
    pass


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def slugify(name: str) -> str:
    return lc.slugify(name, fallback="marca")


def _subdirs(lib_dir: Path):
    """Dirs/arquivos fixos do grid store. As pastas por-marca são dinâmicas
    (uma por slug de marca) e ficam fora desta tupla."""
    return (lib_dir / "rules", lib_dir / "calendar", lib_dir / "mockups",
            lib_dir / ".trash", lib_dir / f"{LIB_DIRNAME}.html")


def _ensure_dirs(lib_dir: Path) -> Path:
    rules, cal, mock, trash, _ = _subdirs(lib_dir)
    lc.ensure_dirs(lib_dir, rules, cal, mock, trash)
    return lib_dir


def find_library_dir(start: Path | None = None,
                     create: bool = True) -> Path | None:
    """
    Resolve o diretório dos grids. Ordem:
      1. $GRIDS_DIR (se setada);
      2. busca pra cima a partir de `start` (default cwd) por um `grids/`
         existente (para na raiz do git/filesystem);
      3. se nada e create=True: cria `<cwd>/grids/`. create=False: None.
    """
    d = lc.find_library_dir(LIB_DIRNAME, ENV_OVERRIDE, start, create)
    if d is not None and create:
        return _ensure_dirs(d)
    return d


def _norm_month(month, year: int | None = None) -> str:
    """Normaliza mês para 'AAAA-MM'. Aceita: 'AAAA-MM', 'MM', 'M', ou nome PT
    ('maio'); year usado quando o mês vem sem ano."""
    s = str(month).strip().lower()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}"
    if s in _PT_MONTHS:
        mm = _PT_MONTHS[s]
    elif s.isdigit() and 1 <= int(s) <= 12:
        mm = int(s)
    else:
        raise InvalidGrid(
            f"Mês '{month}' inválido — use 'AAAA-MM', número 1-12 ou nome "
            f"(ex.: 'maio').")
    if year is None:
        raise InvalidGrid(
            f"Mês '{month}' sem ano — informe year ou use 'AAAA-MM'.")
    return f"{int(year):04d}-{mm:02d}"


def _seed() -> dict:
    """Lê grids.seed.json DE FATO (não .exists()). Estrutura: {grids:[...]}."""
    data = lc.read_json_strict(_SEED_FILE)
    if not isinstance(data, dict):
        raise GridError(
            f"grids.seed.json malformado em {_SEED_FILE} — esperado objeto "
            f"com 'grids'.")
    data.setdefault("grids", [])
    return data


# --------------------------------------------------------------------------- #
# bootstrap / lazy-ensure
# --------------------------------------------------------------------------- #
def _grid_path(lib_dir: Path, brand: str, month: str) -> Path:
    return Path(lib_dir) / slugify(brand) / f"{month}.json"


def bootstrap(lib_dir: Path, _render: bool = True) -> dict:
    """
    Semeia o workspace na 1ª vez:
      - grids do seed (1 JSON por marca-mês) se nenhum grid existe ainda;
      - regras por marca (`rules-seed/*.md` -> `rules/`), só as ausentes;
      - calendário comemorativo (`calendar-seed/*.md` -> `calendar/`), idem.
    Idempotente: nunca sobrescreve arquivo existente. Regras e calendário são
    copiados SEMPRE que faltam (responsabilidade distinta dos grids — mesma
    lógica de thumbnails/fotos no style/product_library).
    Retorna {grids, rules:{...}, calendar:{...}}.
    """
    lib_dir = _ensure_dirs(Path(lib_dir))
    rules_dir, cal_dir, _, _, _ = _subdirs(lib_dir)

    # Validar seed lendo DE FATO (não .exists()).
    try:
        _seed()
    except (OSError, ValueError) as e:
        raise GridError(
            f"grids.seed.json ilegível em {_CORE_DIR} ({e!r}) — plugin mal "
            f"empacotado ou ambiente bloqueando acesso a arquivo.") from e

    # Regras + calendário: disciplina anti-stat-mentiroso do _libcommon.
    # raise_on_empty=False: o seed PODE legitimamente ter 0 arquivos numa
    # instalação enxuta; o que não pode é o os.listdir do plugin dir falhar
    # silenciosamente (isso copy_seed_assets levanta de qualquer forma).
    rules_res = lc.copy_seed_assets(
        _RULES_SEED_DIR, rules_dir, exts={".md"},
        error_cls=GridError, label="rules-seed", raise_on_empty=False)
    cal_res = lc.copy_seed_assets(
        _CALENDAR_SEED_DIR, cal_dir, exts={".md"},
        error_cls=GridError, label="calendar-seed", raise_on_empty=False)

    # Guard de idempotência: grids só são semeados uma vez.
    if _has_any_grid(lib_dir):
        if _render:
            render_grids(lib_dir)
        return {"grids": 0, "rules": rules_res, "calendar": cal_res}

    seed = _seed()
    ng = 0
    for g in seed.get("grids", []):
        b, m = g.get("brand"), g.get("month")
        if not b or not m:
            continue
        dest = _grid_path(lib_dir, b, m)
        if dest.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        lc.atomic_write(dest, json.dumps(g, ensure_ascii=False, indent=2) + "\n")
        ng += 1
    if _render:
        render_grids(lib_dir)
    return {"grids": ng, "rules": rules_res, "calendar": cal_res}


def _ensure_ready(lib_dir: Path | None = None) -> Path:
    """Lazy-ensure: resolve a pasta (criando se preciso) e roda bootstrap
    (idempotente, sem render). Workspace vira fonte única ANTES de
    exibir/curar/mutar — elimina o fallback-fantasma de seed."""
    lib_dir = _ensure_dirs(
        find_library_dir() if lib_dir is None else Path(lib_dir))
    bootstrap(lib_dir, _render=False)
    return lib_dir


# --------------------------------------------------------------------------- #
# leitura (pura: zero-config, cai no seed)
# --------------------------------------------------------------------------- #
def _brand_dirs(lib_dir: Path):
    for child in sorted(Path(lib_dir).iterdir()):
        if child.is_dir() and child.name not in _RESERVED:
            yield child


def _has_any_grid(lib_dir: Path) -> bool:
    for bd in _brand_dirs(lib_dir):
        if any(bd.glob("*.json")):
            return True
    return False


def _read_grids(lib_dir: Path) -> list[dict]:
    out: list[dict] = []
    for bd in _brand_dirs(lib_dir):
        for fp in sorted(bd.glob("*.json")):
            try:
                out.append(json.loads(fp.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError):
                continue
    return out


def _resolve(lib_dir) -> tuple[list[dict], str]:
    if lib_dir is None:
        lib_dir = find_library_dir(create=False)
    if lib_dir is not None:
        items = _read_grids(Path(lib_dir))
        if items:
            return items, "workspace"
    return _seed().get("grids", []), "seed"


def _sort_key(g: dict):
    return (g.get("brand", ""), g.get("month", ""))


def list_grids(brand=None, lib_dir: Path | None = None) -> list[dict]:
    """Lista grids (resumo). Filtra por marca (slug/nome) se dado."""
    items, _ = _resolve(lib_dir)
    if brand is not None:
        bslug = slugify(brand)
        items = [g for g in items if slugify(g.get("brand", "")) == bslug]
    return [
        {"brand": g.get("brand"), "month": g.get("month"),
         "focusProducts": g.get("focusProducts", []),
         "posts": sum(len(w.get("days", [])) for w in g.get("weeks", []))}
        for g in sorted(items, key=_sort_key)
    ]


def get_grid(brand, month, lib_dir: Path | None = None) -> dict:
    """Grid completo de uma marca-mês. month aceita 'AAAA-MM' ou nome/num
    (precisa do ano embutido ou via 'AAAA-MM')."""
    items, _ = _resolve(lib_dir)
    bslug = slugify(brand)
    try:
        m = _norm_month(month)
    except InvalidGrid:
        m = str(month).strip()
    for g in items:
        if slugify(g.get("brand", "")) == bslug and g.get("month") == m:
            return g
    raise GridNotFound(
        f"Grid '{brand}/{month}' não encontrado (use list_grids / --list).")


# --------------------------------------------------------------------------- #
# construção de esqueleto (calendário do mês, domingo-primeiro)
# --------------------------------------------------------------------------- #
def _empty_day(date_iso: str) -> dict:
    d = datetime.strptime(date_iso, "%Y-%m-%d")
    # weekday(): seg=0..dom=6 -> nosso índice dom=0..sab=6
    dow_idx = (d.weekday() + 1) % 7
    return {
        "date": date_iso,
        "dow": _DOW[dow_idx],
        "channel": None,
        "approach": None,
        "product": None,
        "subject": None,
        "ref": None,
        "lettering": {},
        "mockup": None,
        "rationale": "",
        "notes": "",
    }


def _build_weeks(year: int, month: int) -> list[dict]:
    """Esqueleto de semanas domingo→sábado, só os dias do próprio mês
    (espelha a planilha: dias de outros meses ficam vazios/ausentes)."""
    cal = calendar.Calendar(firstweekday=6)  # 6 = domingo
    weeks: list[dict] = []
    for i, week in enumerate(cal.monthdatescalendar(year, month), start=1):
        days = [_empty_day(d.isoformat()) for d in week if d.month == month]
        if days:
            weeks.append({"n": i, "days": days})
    # renumera sequencialmente (semanas sem dia do mês foram puladas)
    for n, w in enumerate(weeks, start=1):
        w["n"] = n
    return weeks


def new_grid(brand: str, month, *, year: int | None = None,
             focus_products: list[str] | None = None,
             lib_dir: Path | None = None, save: bool = True) -> dict:
    """Cria um grid vazio (esqueleto semanal do mês) pra preencher
    conversacionalmente ou via ingestão. month: 'AAAA-MM' ou núm/nome+year."""
    m = _norm_month(month, year)
    yy, mm = int(m[:4]), int(m[5:7])
    grid = {
        "schemaVersion": SCHEMA_VERSION,
        "brand": slugify(brand),
        "month": m,
        "focusProducts": list(focus_products or []),
        "weeks": _build_weeks(yy, mm),
        "createdAt": lc.now(),
        "updatedAt": lc.now(),
    }
    if save:
        return save_grid(grid, lib_dir=lib_dir)
    return grid


# --------------------------------------------------------------------------- #
# escrita
# --------------------------------------------------------------------------- #
def _validate_grid(grid: dict) -> None:
    if not isinstance(grid, dict):
        raise InvalidGrid("grid não é um objeto.")
    if not grid.get("brand"):
        raise InvalidGrid("grid sem 'brand'.")
    if not grid.get("month"):
        raise InvalidGrid("grid sem 'month'.")
    if not re.fullmatch(r"\d{4}-\d{2}", str(grid["month"])):
        raise InvalidGrid(
            f"month '{grid['month']}' fora do formato 'AAAA-MM'.")
    if not isinstance(grid.get("weeks", []), list):
        raise InvalidGrid("grid['weeks'] deve ser lista.")


def save_grid(grid: dict, *, lib_dir: Path | None = None) -> dict:
    """Grava o grid canônico (escrita atômica) e regenera o HTML. Fonte única
    — NUNCA editar o HTML; sempre passar por aqui."""
    _validate_grid(grid)
    lib_dir = _ensure_ready(lib_dir)
    grid = dict(grid)
    grid.setdefault("schemaVersion", SCHEMA_VERSION)
    grid["brand"] = slugify(grid["brand"])
    grid.setdefault("createdAt", lc.now())
    grid["updatedAt"] = lc.now()
    dest = _grid_path(lib_dir, grid["brand"], grid["month"])
    dest.parent.mkdir(parents=True, exist_ok=True)
    lc.atomic_write(dest, json.dumps(grid, ensure_ascii=False, indent=2) + "\n")
    render_grids(lib_dir)
    return grid


def delete_grid(brand, month, *, lib_dir: Path | None = None) -> dict:
    """Soft-delete: move o JSON pra .trash/ (recuperável)."""
    lib_dir = _ensure_ready(lib_dir)
    _, _, _, trash_dir, _ = _subdirs(lib_dir)
    m = _norm_month(month) if not re.fullmatch(
        r"\d{4}-\d{2}", str(month)) else str(month)
    fp = _grid_path(lib_dir, brand, m)
    if not fp.is_file():
        raise GridNotFound(f"Grid '{brand}/{month}' não encontrado.")
    trash_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = trash_dir / f"grid.{slugify(brand)}.{m}.{stamp}.json"
    os.replace(fp, dest)
    render_grids(lib_dir)
    return {"deleted": f"{slugify(brand)}/{m}.json", "trash": str(dest)}


# --------------------------------------------------------------------------- #
# operações de post (edição conversacional — reescrevem o JSON, nunca o HTML)
# --------------------------------------------------------------------------- #
def _find_day(grid: dict, date_iso: str):
    for w in grid.get("weeks", []):
        for d in w.get("days", []):
            if d.get("date") == date_iso:
                return d
    raise GridNotFound(
        f"Dia '{date_iso}' não existe no grid {grid.get('brand')}/"
        f"{grid.get('month')}.")


def _content(day: dict) -> dict:
    return {k: day.get(k) for k in _POST_FIELDS}


def _clear(day: dict) -> None:
    for k in _POST_FIELDS:
        day[k] = {} if k == "lettering" else (
            "" if k in ("rationale", "notes") else None)


def move_post(brand, month, src_date: str, dst_date: str, *,
              lib_dir: Path | None = None) -> dict:
    """Move o conteúdo do post de src_date pra dst_date; src fica vazio
    (espelha 'puxa o do dia 10 pra amanhã' da Estela). dst é sobrescrito."""
    grid = get_grid(brand, month, lib_dir)
    src, dst = _find_day(grid, src_date), _find_day(grid, dst_date)
    content = _content(src)
    for k, v in content.items():
        dst[k] = v
    _clear(src)
    return save_grid(grid, lib_dir=lib_dir)


def swap_posts(brand, month, date_a: str, date_b: str, *,
               lib_dir: Path | None = None) -> dict:
    """Troca o conteúdo de dois dias (mantém data/dow de cada slot)."""
    grid = get_grid(brand, month, lib_dir)
    a, b = _find_day(grid, date_a), _find_day(grid, date_b)
    ca, cb = _content(a), _content(b)
    for k in _POST_FIELDS:
        a[k], b[k] = cb[k], ca[k]
    return save_grid(grid, lib_dir=lib_dir)


def set_post(brand, month, date: str, *, lib_dir: Path | None = None,
             **fields) -> dict:
    """Edita campos de um post. Só os de _POST_FIELDS; data/dow são imutáveis."""
    bad = [k for k in fields if k not in _POST_FIELDS]
    if bad:
        raise InvalidGrid(
            f"Campos não editáveis: {', '.join(bad)}. "
            f"Editáveis: {', '.join(_POST_FIELDS)}.")
    grid = get_grid(brand, month, lib_dir)
    day = _find_day(grid, date)
    day.update(fields)
    return save_grid(grid, lib_dir=lib_dir)


def clear_post(brand, month, date: str, *,
                lib_dir: Path | None = None) -> dict:
    """Esvazia um post (slot vira vazio, data/dow preservados)."""
    grid = get_grid(brand, month, lib_dir)
    _clear(_find_day(grid, date))
    return save_grid(grid, lib_dir=lib_dir)


# --------------------------------------------------------------------------- #
# ingestão das planilhas históricas (Fase 1 — só 2026, valida o modelo)
# --------------------------------------------------------------------------- #
def _load_openpyxl():
    try:
        import openpyxl  # noqa
    except ImportError as e:
        raise GridError(
            "openpyxl ausente — `pip install -r \"$CORE/requirements.txt\"` "
            "(necessário só para ingest_xlsx).") from e
    return openpyxl


def xlsx_sheets(path: str) -> list[str]:
    """Lista as abas de um .xlsx (pra escolher qual ingerir)."""
    openpyxl = _load_openpyxl()
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        return list(wb.sheetnames)
    finally:
        wb.close()


_URL_RE = re.compile(r"https?://\S+")
_TELA_RE = re.compile(r"TELA\s*\d+\s*:", re.IGNORECASE)
_LETTER_RE = re.compile(
    r"LETTERING\s+([A-ZÇÃÕÁÉÍÓÚÂÊÔ]+)\s*:\s*(.*)", re.IGNORECASE)


def _parse_story(blob: str) -> dict:
    """Parser pragmático do blob STORY da 'Briefing Design' → lettering/telas/
    refs. Não busca perfeição (Fase 1 valida o modelo); guarda o cru também."""
    text = str(blob or "").strip()
    if not text:
        return {}
    refs = _URL_RE.findall(text)
    telas = [t.strip() for t in _TELA_RE.split(text)[1:]] if _TELA_RE.search(text) else []
    lettering: dict = {}
    for m in _LETTER_RE.finditer(text):
        lettering[m.group(1).strip().lower()] = m.group(2).strip()
    out: dict = {"raw": text}
    if refs:
        out["refs"] = refs
    if telas:
        out["telas"] = telas
    if lettering:
        out.update(lettering)
    return out


def _cellval(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def ingest_xlsx(path: str, *, sheet: str, brand: str, month,
                year: int = INGEST_YEAR, lib_dir: Path | None = None) -> dict:
    """
    Ingere UMA aba de uma planilha histórica → grid canônico (marca-mês).

    Escopo travado (Lucas 2026-05-18): só **2026**. `year` != 2026 levanta —
    o histórico 2025 fica fora; já valida o modelo com o ano corrente.

    Como o ano não está no nome de aba na planilha de Estratégia, `sheet`,
    `brand`, `month` e `year` são EXPLÍCITOS (use `xlsx_sheets()` p/ escolher).
    Detecta o layout pelo rótulo da coluna A das linhas:
      - "ABORDAGEM" → Estratégia Mensal (PRODUTO + ABORDAGEM por dia);
      - "STORY"     → Briefing Design (PRODUTO + bloco STORY por dia).
    Mapeia colunas B..H = DOMINGO..SÁBADO; números de dia viram datas.
    """
    if int(year) != INGEST_YEAR:
        raise GridError(
            f"Ingestão limitada a {INGEST_YEAR} (Fase 1). year={year} fora "
            f"de escopo — o histórico 2025 não entra.")
    m = _norm_month(month, year)
    yy, mm = int(m[:4]), int(m[5:7])
    openpyxl = _load_openpyxl()
    wb = openpyxl.load_workbook(path, data_only=True)
    try:
        if sheet not in wb.sheetnames:
            raise GridError(
                f"Aba '{sheet}' não existe em {path}. "
                f"Abas: {', '.join(wb.sheetnames)}")
        ws = wb[sheet]
        rows = [[c.value for c in row] for row in
                ws.iter_rows(min_row=1, max_row=min(ws.max_row, 60),
                             max_col=26)]
    finally:
        wb.close()

    grid = new_grid(brand, m, focus_products=None, lib_dir=lib_dir,
                    save=False)
    by_date = {d["date"]: d for w in grid["weeks"] for d in w["days"]}

    def col_to_date(ci: int, day_num: int):
        try:
            return datetime(yy, mm, day_num).strftime("%Y-%m-%d")
        except ValueError:
            return None

    n = len(rows)
    for i in range(n):
        row = rows[i]
        label = _cellval(row[0]).upper() if row else ""
        if label not in ("PRODUTO",):
            continue
        # Linha PRODUTO: achar a linha de NÚMEROS logo acima (1-2 linhas).
        daynum_row = None
        for back in (1, 2):
            if i - back >= 0:
                cand = rows[i - back]
                nums = [(_cellval(cand[c])) for c in range(1, 8)]
                if any(x.isdigit() for x in nums):
                    daynum_row = cand
                    break
        if daynum_row is None:
            continue
        product_row = row
        # Linha de baixo: ABORDAGEM (estratégia) ou STORY (briefing design).
        kind_row = rows[i + 1] if i + 1 < n else None
        kind_label = _cellval(kind_row[0]).upper() if kind_row else ""
        for c in range(1, 8):  # B..H
            dn = _cellval(daynum_row[c])
            if not dn.isdigit():
                continue
            date_iso = col_to_date(c, int(dn))
            if not date_iso or date_iso not in by_date:
                continue
            day = by_date[date_iso]
            prod = _cellval(product_row[c])
            if prod:
                day["subject"] = prod
            if kind_label == "ABORDAGEM":
                ab = _cellval(kind_row[c])
                if ab:
                    day["approach"] = ab.upper()
            elif kind_label == "STORY":
                day["channel"] = "story"
                story = _parse_story(kind_row[c])
                if story:
                    day["lettering"] = story

    grid["ingestedFrom"] = {
        "file": Path(path).name, "sheet": sheet,
        "at": lc.now(),
    }
    return save_grid(grid, lib_dir=lib_dir)


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #
def render_grids(lib_dir: Path | None = None,
                 template_path: Path | None = None) -> Path:
    """Lê o template, injeta {grids:[...]} (workspace ou seed) e escreve
    `<lib_dir>/grids.html`. Sempre derivado — nunca lido como dado."""
    lib_dir = _ensure_ready(lib_dir)
    grids = sorted(_resolve(lib_dir)[0], key=_sort_key)
    payload = json.dumps({"grids": grids}, ensure_ascii=False)
    tpl = Path(template_path or _TEMPLATE_FILE).read_text(encoding="utf-8")
    injected = lc.inject_placeholder(tpl, _PLACEHOLDER, payload, GridError)
    _, _, _, _, html_path = _subdirs(lib_dir)
    lc.atomic_write(html_path, injected)
    return html_path


def open_grids(lib_dir: Path | None = None) -> Path:
    """Regenera e devolve o caminho do grids.html (a skill manda abrir)."""
    return render_grids(lib_dir)

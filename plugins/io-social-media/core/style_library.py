"""
style_library — biblioteca de estilos visuais reutilizáveis (InsideOut).

Contrato único compartilhado pelas skills `image-generation` e `style-gallery`.

Princípios (ver plano swift-prancing-gosling):
- Os dados vivem na PASTA DE TRABALHO do usuário, 1 arquivo JSON por estilo
  (`<workspace>/style-gallery/styles/<slug>.json`) — nunca no diretório do
  plugin (read-only/efêmero no Cowork).
- A galeria HTML é SEMPRE derivada (gerada do JSON) — nunca fonte de dado.
- Escrita atômica; delete é soft (.trash/); nada de "apagar tudo".
- Sem workspace, cai no seed embarcado (read-only) — zero-config mantém os
  5 exemplos funcionando.

Este módulo só é importado; não tem efeitos colaterais no import.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1
LIB_DIRNAME = "style-gallery"
ENV_OVERRIDE = "STYLE_GALLERY_DIR"

# Espelham gallery-template.html (CATEGORIES/CANONICAL_TAGS no <script>).
# Se mudar lá, mudar aqui (e vice-versa). Taxonomia de social/PR — Inside Out.
CATEGORIES = ["Produto", "Campanha", "Pessoas", "Editorial", "Evento", "Imprensa"]
CANONICAL_TAGS = {
    "Produto": ["packshot", "flat-lay", "still-life", "em-cenario",
                "macro-textura", "lancamento", "gerado-por-ia"],
    "Campanha": ["sazonal", "data-comemorativa", "key-visual", "teaser",
                 "oferta", "flat-lay", "feito-a-mao", "gerado-por-ia"],
    "Pessoas": ["beauty", "retrato", "lifestyle", "close-pele",
                "kol-influencer", "diversidade"],
    "Editorial": ["moodboard", "colagem", "color-story", "capa-editorial",
                  "serie", "flat-lay"],
    "Evento": ["cobertura", "cenografia", "bastidores", "convite", "press-trip"],
    "Imprensa": ["clipping", "card-resultado", "citacao", "anuncio-na-midia",
                 "infografico"],
}

# NUNCA usar .resolve() aqui: em apps empacotados (UWP/MSIX — Claude Desktop)
# .resolve() segue a junção do pacote e devolve o caminho interno
# (AppData\Local\Packages\...) que o processo NÃO consegue abrir/stat, mesmo
# com listdir funcionando. Isso fazia is_file()/is_dir() mentirem "False" e a
# cópia de thumbnails sumir silenciosamente. __file__ já é absoluto (a skill
# injeta ${CLAUDE_PLUGIN_ROOT}/core absoluto no sys.path), então .parent basta.
_CORE_DIR = Path(__file__).parent
_SEED_FILE = _CORE_DIR / "styles.seed.json"
_TEMPLATE_FILE = _CORE_DIR / "gallery-template.html"
_PLACEHOLDER = "/*__STYLES_JSON__*/[]"


class StyleLibraryError(Exception):
    """Erro base da biblioteca."""


class StyleNotFound(StyleLibraryError):
    pass


class InvalidCategory(StyleLibraryError):
    pass


class InvalidTag(StyleLibraryError):
    pass


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(name: str) -> str:
    n = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    n = re.sub(r"[^a-zA-Z0-9]+", "-", n).strip("-").lower()
    n = re.sub(r"-{2,}", "-", n)
    return n or "style"


def _atomic_write(path: Path, text: str) -> None:
    """Escreve via arquivo temporário no mesmo diretório + os.replace (atômico)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _subdirs(lib_dir: Path):
    return (lib_dir / "styles", lib_dir / "thumbnails",
            lib_dir / ".trash", lib_dir / f"{LIB_DIRNAME}.html")


def _ensure_dirs(lib_dir: Path) -> Path:
    styles, thumbs, trash, _ = _subdirs(lib_dir)
    for d in (lib_dir, styles, thumbs, trash):
        d.mkdir(parents=True, exist_ok=True)
    return lib_dir


# --------------------------------------------------------------------------- #
# descoberta / bootstrap
# --------------------------------------------------------------------------- #
def find_library_dir(start: Path | None = None, create: bool = True) -> Path | None:
    """
    Resolve o diretório da biblioteca. Ordem:
      1. $STYLE_GALLERY_DIR (se setado).
      2. Busca pra cima a partir de `start` (default cwd) por uma
         `style-gallery/` existente; para na raiz do git ou do filesystem.
      3. Se nada e create=True: cria `<cwd>/style-gallery/`.
         Se create=False: retorna None.
    """
    env = os.environ.get(ENV_OVERRIDE)
    if env:
        p = Path(env).expanduser().resolve()
        return _ensure_dirs(p) if create else (p if p.exists() else None)

    start = Path(start).resolve() if start else Path.cwd().resolve()
    cur = start
    while True:
        cand = cur / LIB_DIRNAME
        if cand.is_dir():
            return cand
        if (cur / ".git").exists() or cur.parent == cur:
            break
        cur = cur.parent

    if create:
        return _ensure_dirs(start / LIB_DIRNAME)
    return None


def _seed_styles() -> list[dict]:
    return json.loads(_SEED_FILE.read_text(encoding="utf-8"))


def bootstrap(lib_dir: Path, _render: bool = True) -> int:
    """
    Se `styles/` não tem nenhum *.json, semeia a partir de styles.seed.json
    (1 arquivo por estilo) e copia os thumbnails do seed. Idempotente:
    nunca sobrescreve arquivo de estilo já existente.
    Retorna quantos estilos foram semeados.

    `_render=False` (uso interno do _ensure_ready) pula o render final pra
    evitar recursão render_gallery → _ensure_ready → bootstrap.
    """
    lib_dir = _ensure_dirs(Path(lib_dir))
    styles_dir, thumbs_dir, _, _ = _subdirs(lib_dir)
    # Empacotamento / acesso: NÃO confiar em .exists()/.is_dir()/.is_file() —
    # em ambiente UWP/MSIX (Claude Desktop) o stat do caminho do plugin falha
    # e pathlib engole o OSError, devolvendo "False" mentiroso. Foi a causa-raiz
    # do bug de thumbnails que sobreviveu a 3 releases: a cópia sumia em
    # silêncio. Aqui: validar lendo de fato + os.listdir + copiar de verdade,
    # e FALHAR ALTO se nada vier — nunca publicar galeria "sem preview" mudo.
    try:
        _seed_styles()  # leitura real de styles.seed.json (não .exists())
    except (OSError, ValueError) as e:
        raise StyleLibraryError(
            f"styles.seed.json ilegível em {_CORE_DIR} ({e!r}) — plugin mal "
            f"empacotado ou ambiente bloqueando acesso a arquivo.") from e
    src_thumbs = _CORE_DIR / "thumbnails"
    try:
        entries = os.listdir(src_thumbs)
    except OSError as e:
        raise StyleLibraryError(
            f"core/thumbnails ilegível em {src_thumbs} ({e!r}) — plugin mal "
            f"empacotado ou ambiente bloqueando acesso a diretório.") from e
    _IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    imgs = [n for n in entries if os.path.splitext(n)[1].lower() in _IMG_EXT]
    # Copia thumbnails ausentes — independente de os styles já existirem
    # (responsabilidades distintas; roda ANTES do guard de idempotência).
    copied = existed = 0
    errors: list[str] = []
    for name in imgs:
        tgt = thumbs_dir / name           # tgt vive no workspace (FS normal)
        if tgt.exists():
            existed += 1
            continue
        try:
            shutil.copy2(src_thumbs / name, tgt)
            copied += 1
        except OSError as e:
            errors.append(f"{name}: {e!r}")
    if imgs and copied == 0 and existed == 0:
        raise StyleLibraryError(
            f"Nenhum dos {len(imgs)} thumbnails do seed chegou ao workspace "
            f"({src_thumbs} -> {thumbs_dir}). Erros: "
            f"{errors or '[sem exceção; provável bloqueio silencioso de '
            f'acesso ao diretório do plugin]'}.")
    # Guard de idempotência: styles só são semeados uma vez.
    if any(styles_dir.glob("*.json")):
        return 0
    seeded = 0
    for s in _seed_styles():
        dest = styles_dir / f"{s['slug']}.json"
        if dest.exists():
            continue
        _atomic_write(dest, json.dumps(s, ensure_ascii=False, indent=2) + "\n")
        seeded += 1
    if _render:
        render_gallery(lib_dir)
    return seeded


def _ensure_ready(lib_dir: Path | None = None) -> Path:
    """Lazy-ensure: resolve a pasta da biblioteca (criando se preciso) e
    chama bootstrap (idempotente, sem render pra não recursar). Garante que o
    workspace seja a fonte única ANTES de exibir/curar/mutar — elimina o
    fallback-fantasma de seed. bootstrap sempre roda: o guard de seed vive
    dentro dele, e a cópia de thumbnails precisa rodar mesmo com styles já
    existentes (ex: thumbs sumidos por mount hostil do Cowork desktop)."""
    lib_dir = _ensure_dirs(find_library_dir() if lib_dir is None else Path(lib_dir))
    bootstrap(lib_dir, _render=False)
    return lib_dir


# --------------------------------------------------------------------------- #
# leitura
# --------------------------------------------------------------------------- #
def _read_workspace(lib_dir: Path) -> list[dict]:
    styles_dir, *_ = _subdirs(lib_dir)
    out = []
    for fp in styles_dir.glob("*.json"):
        try:
            out.append(json.loads(fp.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return out


def _resolve_read(lib_dir):
    """Retorna (lista_de_estilos, origem). origem: 'workspace' ou 'seed'."""
    if lib_dir is None:
        lib_dir = find_library_dir(create=False)
    if lib_dir is not None:
        styles = _read_workspace(Path(lib_dir))
        if styles:
            return styles, "workspace"
    return _seed_styles(), "seed"


def list_styles(lib_dir: Path | None = None) -> list[dict]:
    styles, _ = _resolve_read(lib_dir)
    return sorted(styles, key=lambda s: s.get("id", 0))


def get_style(ref, lib_dir: Path | None = None) -> dict:
    """ref aceita id (int / dígito) ou slug (str)."""
    styles, _ = _resolve_read(lib_dir)
    s = str(ref).strip()
    if s.isdigit():
        rid = int(s)
        for st in styles:
            if st.get("id") == rid:
                return st
    for st in styles:
        if st.get("slug") == s or st.get("name") == ref:
            return st
    raise StyleNotFound(f"Estilo '{ref}' não encontrado (use --list para ver os disponíveis).")


# --------------------------------------------------------------------------- #
# validação / escrita
# --------------------------------------------------------------------------- #
def _validate(category: str, tags: list[str]) -> None:
    if category not in CATEGORIES:
        raise InvalidCategory(
            f"Categoria '{category}' inválida. Use uma de: {', '.join(CATEGORIES)}")
    allowed = set(CANONICAL_TAGS.get(category, []))
    bad = [t for t in (tags or []) if t not in allowed]
    if bad:
        raise InvalidTag(
            f"Tag(s) {bad} inválida(s) para '{category}'. "
            f"Permitidas: {', '.join(sorted(allowed))}")


def _unique_slug(styles_dir: Path, base: str) -> str:
    slug, i = base, 2
    while (styles_dir / f"{slug}.json").exists():
        slug = f"{base}-{i}"
        i += 1
    return slug


def _next_id(styles: list[dict]) -> int:
    return 1 + max((s.get("id", 0) for s in styles), default=0)


def add_style(name: str, prompt: str, *, category: str, tags: list[str] | None = None,
              example_use: str = "", thumbnail: str | None = None,
              lib_dir: Path | None = None) -> dict:
    """Cria um estilo novo. Nunca sobrescreve outro (slug único, id monotônico)."""
    tags = list(tags or [])
    _validate(category, tags)
    lib_dir = _ensure_ready(lib_dir)  # materializa os 5 exemplos antes -> id segue em #6
    styles_dir, thumbs_dir, _, _ = _subdirs(lib_dir)

    slug = _unique_slug(styles_dir, slugify(name))
    thumb_rel = ""
    if thumbnail:
        src = Path(thumbnail)
        if src.is_file():
            ext = src.suffix.lower() or ".png"
            shutil.copy2(src, thumbs_dir / f"{slug}{ext}")
            thumb_rel = f"thumbnails/{slug}{ext}"
    ts = _now()
    style = {
        "schemaVersion": SCHEMA_VERSION,
        "id": _next_id(_read_workspace(lib_dir)),
        "slug": slug,
        "name": name,
        "category": category,
        "tags": tags,
        "thumbnail": thumb_rel,
        "prompt": prompt,
        "exampleUse": example_use,
        "createdAt": ts,
        "updatedAt": ts,
    }
    _atomic_write(styles_dir / f"{slug}.json",
                  json.dumps(style, ensure_ascii=False, indent=2) + "\n")
    render_gallery(lib_dir)
    return style


def _find_workspace_file(lib_dir: Path, ref) -> Path:
    styles_dir, *_ = _subdirs(lib_dir)
    s = str(ref).strip()
    for fp in styles_dir.glob("*.json"):
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if (s.isdigit() and d.get("id") == int(s)) or d.get("slug") == s or d.get("name") == ref:
            return fp
    raise StyleNotFound(
        f"Estilo '{ref}' não encontrado na biblioteca "
        f"(use list_styles / get_style.py --list para ver os disponíveis).")


def update_style(ref, *, lib_dir: Path | None = None, **fields) -> dict:
    """Atualiza campos de um estilo do workspace. slug e id são estáveis."""
    lib_dir = _ensure_ready(lib_dir)  # 5 exemplos viram arquivos reais editáveis
    fp = _find_workspace_file(Path(lib_dir), ref)
    style = json.loads(fp.read_text(encoding="utf-8"))
    for k in ("schemaVersion", "id", "slug", "createdAt"):
        fields.pop(k, None)  # imutáveis
    style.update(fields)
    _validate(style.get("category"), style.get("tags") or [])
    style["updatedAt"] = _now()
    _atomic_write(fp, json.dumps(style, ensure_ascii=False, indent=2) + "\n")
    render_gallery(lib_dir)
    return style


def delete_style(ref, *, lib_dir: Path | None = None) -> dict:
    """Soft-delete: move o JSON pra .trash/ (recuperável). Não apaga a thumbnail."""
    lib_dir = _ensure_ready(lib_dir)
    fp = _find_workspace_file(lib_dir, ref)
    _, _, trash_dir, _ = _subdirs(lib_dir)
    trash_dir.mkdir(parents=True, exist_ok=True)
    dest = trash_dir / f"{fp.stem}.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    os.replace(fp, dest)
    render_gallery(lib_dir)
    return {"deleted": fp.name, "trash": str(dest)}


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #
def render_gallery(lib_dir: Path | None = None,
                   template_path: Path | None = None) -> Path:
    """
    Lê o template, injeta os estilos (workspace ou seed) e escreve
    `<lib_dir>/style-gallery.html`. Sempre derivado — nunca lido como dado.
    """
    lib_dir = _ensure_ready(lib_dir)  # materializa os 5 exemplos -> HTML mostra reais c/ thumb
    styles = sorted(_resolve_read(lib_dir)[0], key=lambda s: s.get("id", 0))
    tpl = Path(template_path or _TEMPLATE_FILE).read_text(encoding="utf-8")
    if _PLACEHOLDER not in tpl:
        raise StyleLibraryError(
            f"Placeholder {_PLACEHOLDER!r} ausente no template — template corrompido.")
    injected = tpl.replace(_PLACEHOLDER, json.dumps(styles, ensure_ascii=False), 1)
    _, _, _, html_path = _subdirs(lib_dir)
    _atomic_write(html_path, injected)
    return html_path


def open_gallery(lib_dir: Path | None = None) -> Path:
    """Regenera e devolve o caminho do HTML (a skill instrui o usuário a abrir)."""
    return render_gallery(lib_dir)

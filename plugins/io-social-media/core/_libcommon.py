"""
_libcommon — primitivos compartilhados entre `style_library` e `product_library`.

Centraliza a **disciplina UWP-safe** que custou 3 releases quando vivia
duplicada (bug de thumbnails 0.3.4/0.3.5, raiz definitiva no 0.3.7):

- NUNCA `.resolve()` em `__file__` de plugin — em app empacotado (UWP/MSIX,
  Claude Desktop) `.resolve()` segue a junção do pacote e devolve o caminho
  interno que o processo não consegue `stat()`; `pathlib` engole o `OSError`
  e `is_file()`/`is_dir()`/`exists()` mentem `False`, sumindo cópia em silêncio.
- No diretório do plugin, desconfiar de TODO stat: `os.listdir` + cópia real +
  **falhar alto** se nada chegou — nunca publicar artefato mudo "sem preview".

Duplicar essa regra em dois arquivos é exatamente o modo de divergência
silenciosa que a fricção do fork `voice-check` registrou (divergiu inferior em
1 dia). Este é o ÚNICO lugar que precisa saber disso.

Sem efeitos colaterais no import.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

# NUNCA usar .resolve() aqui. __file__ já vem absoluto (a skill injeta
# ${CLAUDE_PLUGIN_ROOT}/core absoluto no sys.path). `style_library` e
# `product_library` vivem ambos em core/, então .parent daqui serve aos dois —
# um único ponto de verdade pra essa regra.
CORE_DIR = Path(__file__).parent

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


class LibCommonError(Exception):
    """Base de erros das bibliotecas (style/product)."""


# --------------------------------------------------------------------------- #
# utilidades puras
# --------------------------------------------------------------------------- #
def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(name: str, fallback: str = "item") -> str:
    n = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    n = re.sub(r"[^a-zA-Z0-9]+", "-", n).strip("-").lower()
    n = re.sub(r"-{2,}", "-", n)
    return n or fallback


def atomic_write(path: Path, text: str) -> None:
    """Escreve via arquivo temporário no mesmo diretório + os.replace (atômico)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def ensure_dirs(*dirs: Path) -> None:
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
# descoberta da biblioteca (workspace = FS normal; .resolve() ok AQUI)
# --------------------------------------------------------------------------- #
def find_library_dir(lib_dirname: str, env_override: str,
                     start: Path | None = None,
                     create: bool = True) -> Path | None:
    """
    Resolve o diretório da biblioteca. Ordem:
      1. $<env_override> (se setado).
      2. Busca pra cima a partir de `start` (default cwd) por uma
         `<lib_dirname>/` existente; para na raiz do git ou do filesystem.
      3. Se nada e create=True: cria `<cwd>/<lib_dirname>/`.
         Se create=False: retorna None.

    .resolve() é usado SÓ aqui porque o alvo é a pasta de trabalho do usuário
    (filesystem normal), nunca o diretório do plugin.
    """
    env = os.environ.get(env_override)
    if env:
        p = Path(env).expanduser().resolve()
        if create:
            p.mkdir(parents=True, exist_ok=True)
            return p
        return p if p.exists() else None

    start = Path(start).resolve() if start else Path.cwd().resolve()
    cur = start
    while True:
        cand = cur / lib_dirname
        if cand.is_dir():
            return cand
        if (cur / ".git").exists() or cur.parent == cur:
            break
        cur = cur.parent

    if create:
        d = start / lib_dirname
        d.mkdir(parents=True, exist_ok=True)
        return d
    return None


# --------------------------------------------------------------------------- #
# leitura/seed à prova de stat-mentiroso do plugin dir
# --------------------------------------------------------------------------- #
def read_json_strict(path: Path):
    """Lê e parseia JSON DE FATO (não `.exists()`). Propaga OSError/ValueError —
    quem chama decide o erro tipado. É a leitura que não confia em stat."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def copy_seed_assets(src_dir: Path, tgt_dir: Path, *, exts: set,
                     error_cls: type, label: str,
                     raise_on_empty: bool = True) -> dict:
    """
    Copia assets ausentes do seed (plugin dir) pro workspace. NÃO confia em
    stat do plugin dir: `os.listdir` + cópia real + **FALHA ALTO** se havia
    assets e nenhum chegou. Esta é a disciplina que matou o bug UWP que
    atravessou 3 releases — não publicar galeria/catálogo mudo em silêncio.

    Retorna {copied, existed, total, errors}. `tgt` vive no workspace
    (FS normal), então `.exists()` nele é confiável.

    `raise_on_empty=False`: não levanta no caso zero-cópia — devolve o
    resultado pra quem chama agregar a decisão de falha-alto (ex.: catálogo
    que copia fotos por subdir produto-a-produto e só falha alto se NENHUM
    subdir trouxe nada).
    """
    src_dir = Path(src_dir)
    tgt_dir = Path(tgt_dir)
    tgt_dir.mkdir(parents=True, exist_ok=True)
    try:
        entries = os.listdir(src_dir)
    except OSError as e:
        raise error_cls(
            f"{label} ilegível em {src_dir} ({e!r}) — plugin mal empacotado "
            f"ou ambiente bloqueando acesso a diretório.") from e
    assets = [n for n in entries if os.path.splitext(n)[1].lower() in exts]
    copied = existed = 0
    errors: list[str] = []
    for name in assets:
        tgt = tgt_dir / name
        if tgt.exists():
            existed += 1
            continue
        try:
            shutil.copy2(src_dir / name, tgt)
            copied += 1
        except OSError as e:
            errors.append(f"{name}: {e!r}")
    if raise_on_empty and assets and copied == 0 and existed == 0:
        raise error_cls(
            f"Nenhum dos {len(assets)} assets do seed chegou ao workspace "
            f"({src_dir} -> {tgt_dir}). Erros: "
            f"{errors or '[sem exceção; provável bloqueio silencioso de '
            f'acesso ao diretório do plugin]'}.")
    return {"copied": copied, "existed": existed,
            "total": len(assets), "errors": errors}


# --------------------------------------------------------------------------- #
# render por placeholder + helpers de workspace
# --------------------------------------------------------------------------- #
def inject_placeholder(tpl_text: str, placeholder: str, payload: str,
                       error_cls: type) -> str:
    if placeholder not in tpl_text:
        raise error_cls(
            f"Placeholder {placeholder!r} ausente no template — "
            f"template corrompido.")
    return tpl_text.replace(placeholder, payload, 1)


def read_workspace_json(dir_: Path) -> list:
    out = []
    for fp in Path(dir_).glob("*.json"):
        try:
            out.append(json.loads(fp.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return out


def unique_slug(dir_: Path, base: str) -> str:
    slug, i = base, 2
    while (Path(dir_) / f"{slug}.json").exists():
        slug = f"{base}-{i}"
        i += 1
    return slug


def next_id(items: list) -> int:
    return 1 + max((s.get("id", 0) for s in items), default=0)


def find_workspace_file(dir_: Path, ref, *, error_cls: type,
                        not_found_msg: str) -> Path:
    s = str(ref).strip()
    for fp in Path(dir_).glob("*.json"):
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if ((s.isdigit() and d.get("id") == int(s))
                or d.get("slug") == s or d.get("name") == ref):
            return fp
    raise error_cls(not_found_msg)

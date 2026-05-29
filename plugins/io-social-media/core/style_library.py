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

A disciplina UWP-safe (nunca `.resolve()` em `__file__` de plugin; desconfiar
de todo stat do plugin dir — `os.listdir` + cópia real + falha alto) vive em
`_libcommon` (um único ponto de verdade, compartilhado com `product_library`).

Este módulo só é importado; não tem efeitos colaterais no import.
"""
from __future__ import annotations

import json
from pathlib import Path

import _libcommon as lc

SCHEMA_VERSION = 1
LIB_DIRNAME = "style-gallery"
ENV_OVERRIDE = "STYLE_GALLERY_DIR"

# Espelham dashboard-template.html (CATEGORIES/CANONICAL_TAGS no <script>).
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

# _CORE_DIR vem de _libcommon (Path(__file__).parent SEM .resolve() — ver lá o
# porquê: junção UWP/MSIX faz .resolve() devolver caminho não-stat-ável).
_CORE_DIR = lc.CORE_DIR
_SEED_FILE = _CORE_DIR / "styles.seed.json"


class StyleLibraryError(lc.LibCommonError):
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
def slugify(name: str) -> str:
    # Mantém o fallback histórico "style" (vs. "item" genérico do _libcommon).
    return lc.slugify(name, fallback="style")


def _subdirs(lib_dir: Path):
    return (lib_dir / "styles", lib_dir / "thumbnails",
            lib_dir / ".trash", lib_dir / f"{LIB_DIRNAME}.html")


def _ensure_dirs(lib_dir: Path) -> Path:
    styles, thumbs, trash, _ = _subdirs(lib_dir)
    lc.ensure_dirs(lib_dir, styles, thumbs, trash)
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
    d = lc.find_library_dir(LIB_DIRNAME, ENV_OVERRIDE, start, create)
    if d is not None and create:
        return _ensure_dirs(d)
    return d


def _seed_styles() -> list[dict]:
    return lc.read_json_strict(_SEED_FILE)


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

    # Empacotamento / acesso: NÃO confiar em stat do plugin dir. Validar lendo
    # de fato + os.listdir + copiar de verdade, FALHAR ALTO se nada vier —
    # nunca publicar galeria "sem preview" mudo. (disciplina em _libcommon)
    try:
        lc.read_json_strict(_SEED_FILE)  # leitura real (não .exists())
    except (OSError, ValueError) as e:
        raise StyleLibraryError(
            f"styles.seed.json ilegível em {_CORE_DIR} ({e!r}) — plugin mal "
            f"empacotado ou ambiente bloqueando acesso a arquivo.") from e

    # Copia thumbnails ausentes — independente de os styles já existirem
    # (responsabilidades distintas; roda ANTES do guard de idempotência).
    lc.copy_seed_assets(_CORE_DIR / "thumbnails", thumbs_dir,
                        exts=lc.IMG_EXT, error_cls=StyleLibraryError,
                        label="core/thumbnails")

    # Guard de idempotência: styles só são semeados uma vez.
    if any(styles_dir.glob("*.json")):
        return 0
    seeded = 0
    for s in _seed_styles():
        dest = styles_dir / f"{s['slug']}.json"
        if dest.exists():
            continue
        lc.atomic_write(dest, json.dumps(s, ensure_ascii=False, indent=2) + "\n")
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
    return lc.read_workspace_json(styles_dir)


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
    raise StyleNotFound(
        f"Estilo '{ref}' não encontrado (use --list para ver os disponíveis).")


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
    return lc.unique_slug(styles_dir, base)


def _next_id(styles: list[dict]) -> int:
    return lc.next_id(styles)


def add_style(name: str, prompt: str, *, category: str, tags: list[str] | None = None,
              example_use: str = "", thumbnail: str | None = None,
              lib_dir: Path | None = None) -> dict:
    """Cria um estilo novo. Nunca sobrescreve outro (slug único, id monotônico)."""
    import shutil

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
    ts = lc.now()
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
    lc.atomic_write(styles_dir / f"{slug}.json",
                    json.dumps(style, ensure_ascii=False, indent=2) + "\n")
    render_gallery(lib_dir)
    return style


def _find_workspace_file(lib_dir: Path, ref) -> Path:
    styles_dir, *_ = _subdirs(lib_dir)
    return lc.find_workspace_file(
        styles_dir, ref, error_cls=StyleNotFound,
        not_found_msg=(
            f"Estilo '{ref}' não encontrado na biblioteca "
            f"(use list_styles / get_style.py --list para ver os disponíveis)."))


def update_style(ref, *, lib_dir: Path | None = None, **fields) -> dict:
    """Atualiza campos de um estilo do workspace. slug e id são estáveis."""
    lib_dir = _ensure_ready(lib_dir)  # 5 exemplos viram arquivos reais editáveis
    fp = _find_workspace_file(Path(lib_dir), ref)
    style = json.loads(fp.read_text(encoding="utf-8"))
    for k in ("schemaVersion", "id", "slug", "createdAt"):
        fields.pop(k, None)  # imutáveis
    style.update(fields)
    _validate(style.get("category"), style.get("tags") or [])
    style["updatedAt"] = lc.now()
    lc.atomic_write(fp, json.dumps(style, ensure_ascii=False, indent=2) + "\n")
    render_gallery(lib_dir)
    return style


def delete_style(ref, *, lib_dir: Path | None = None) -> dict:
    """Soft-delete: move o JSON pra .trash/ (recuperável). Não apaga a thumbnail."""
    import os
    from datetime import datetime, timezone

    lib_dir = _ensure_ready(lib_dir)
    fp = _find_workspace_file(lib_dir, ref)
    _, _, trash_dir, _ = _subdirs(lib_dir)
    trash_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = trash_dir / f"{fp.stem}.{stamp}.json"
    os.replace(fp, dest)
    render_gallery(lib_dir)
    return {"deleted": fp.name, "trash": str(dest)}


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #
def render_gallery(lib_dir: Path | None = None) -> Path:
    """Regenera o painel unificado da InsideOut (`insideout-painel.html`) com a
    aba Estilos. A galeria virou uma aba do painel único; este wrapper preserva
    o nome histórico que o CRUD/bootstrap chamam. O painel é gravado na raiz
    comum das três pastas-domínio, não em `style-gallery/`. Sempre derivado."""
    lib_dir = _ensure_ready(lib_dir)  # materializa os 5 exemplos + thumbnails
    import dashboard  # import tardio: quebra o ciclo dashboard <-> libs
    return dashboard.render_dashboard(active_tab="styles", style_dir=lib_dir)


def open_gallery(lib_dir: Path | None = None) -> Path:
    """Regenera e devolve o caminho do painel (a skill instrui a abrir na aba
    Estilos via `#styles`)."""
    return render_gallery(lib_dir)

"""
dashboard — orquestrador do painel único da InsideOut (estilos × produtos × grid).

Reúne as três visualizações que antes eram HTMLs separados
(`gallery-template`/`product-catalog-template`/`grid-template`) num único
arquivo standalone (`dashboard-template.html`) com abas por tipo + seletor de
marca global. Substitui os três templates antigos.

Direção de dependência (importante): este módulo depende das três libs; as três
NÃO dependem entre si. `style_library`/`product_library`/`grid_library` chamam
de volta `dashboard.render_dashboard` por **import tardio** (dentro de
`render_*`/`open_*`) — assim o ciclo de import nunca fecha em tempo de import.

Não reimplementa leitura: reusa as funções públicas de cada lib
(`list_styles`, `list_brands`/`list_products`, `list_grids_full`). A disciplina
UWP-safe (nunca `.resolve()` em `__file__` de plugin) vive em `_libcommon`;
`.resolve()`/`relpath` aqui só tocam a pasta de trabalho (FS normal), nunca o
diretório do plugin.

Sem efeitos colaterais no import.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import _libcommon as lc
import style_library as sl
import product_library as pl
import grid_library as gl

ACTIVE_TABS = ("styles", "products", "grid")
_HTML_NAME = "insideout-painel.html"
_TEMPLATE_FILE = lc.CORE_DIR / "dashboard-template.html"   # CORE_DIR: sem .resolve(__file__)
_PLACEHOLDER = "/*__DASHBOARD_JSON__*/null"


class DashboardError(lc.LibCommonError):
    """Erro base do painel unificado."""


# --------------------------------------------------------------------------- #
# materialização das três libs (seed idempotente, sem render por lib)
# --------------------------------------------------------------------------- #
def _ensure_all(style_dir=None, product_dir=None, grid_dir=None):
    """Resolve e materializa o seed das três libs (idempotente). Devolve os três
    diretórios resolvidos. `_render=False` em cada bootstrap evita recursão de
    volta pro dashboard."""
    sdir = sl.find_library_dir(create=True) if style_dir is None else Path(style_dir)
    sl.bootstrap(sdir, _render=False)
    pdir = pl.find_library_dir(create=True) if product_dir is None else Path(product_dir)
    pl.bootstrap(pdir, _render=False)
    gdir = gl.find_library_dir(create=True) if grid_dir is None else Path(grid_dir)
    gl.bootstrap(gdir, _render=False)
    return sdir, pdir, gdir


def _rel_prefix(asset_dir: Path, home: Path) -> str:
    """Prefixo relativo (com '/' de URL) da pasta-domínio em relação ao home do
    painel. No caso comum (pastas irmãs sob o workspace) vira o nome da pasta
    (ex.: 'style-gallery'). Workspace = FS normal, relpath é seguro aqui."""
    rel = os.path.relpath(str(asset_dir), str(home))
    return rel.replace(os.sep, "/")


def _reprefix(path: str | None, prefix: str) -> str | None:
    """Reescreve um caminho de asset relativo à pasta-domínio para relativo ao
    home do painel: 'thumbnails/x.png' -> '<prefix>/thumbnails/x.png'.
    Deixa absolutos/URLs intactos."""
    if not path:
        return path
    p = str(path).replace("\\", "/")
    if p.startswith(("http://", "https://", "data:", "/")) or (len(p) > 1 and p[1] == ":"):
        return p
    return f"{prefix}/{p}" if prefix not in ("", ".") else p


def _resolve_grid_asset(path: str | None, gdir: Path, home: Path) -> str | None:
    """Resolve o caminho de um asset do grid (mockup de imagem OU vídeo) pro
    ARQUIVO real e devolve-o relativo ao home do painel (com '/'). Tolerante à
    origem do caminho — pode ter vindo do fluxo canônico (relativo a grids/:
    'mockups/...'), de um caminho visto da raiz do workspace ('grids/mockups/...'),
    de um arquivo ad-hoc ('outputs/...'), ou absoluto. URLs/data ficam intactas.
    Conserta de uma vez o sumiço (caminho que não resolve) e a duplicação
    'grids/grids/...' que o prefixo cego do _reprefix gerava.

    Workspace = FS normal, então `.is_file()`/relpath são confiáveis aqui (a
    disciplina UWP de nunca confiar em stat vale só pro diretório do plugin)."""
    if not path:
        return path
    p = str(path).replace("\\", "/")
    if p.startswith(("http://", "https://", "data:")):
        return p
    pp = Path(p)
    if pp.is_absolute() or (len(p) > 1 and p[1] == ":"):
        candidates = [pp]
    else:
        candidates = [Path(gdir) / p,   # canônico: relativo a grids/
                      Path(home) / p]   # relativo ao workspace (grids/..., outputs/...)
    for c in candidates:
        try:
            if c.is_file():
                return os.path.relpath(str(c), str(home)).replace(os.sep, "/")
        except OSError:
            continue
    # não achou o arquivo — prefixo cego antigo (sem regredir o que ainda não existe)
    return _reprefix(p, _rel_prefix(Path(gdir), Path(home)))


# --------------------------------------------------------------------------- #
# composição do payload
# --------------------------------------------------------------------------- #
def build_payload(*, active_tab="styles",
                  style_dir=None, product_dir=None, grid_dir=None,
                  home: Path | None = None) -> dict:
    """Lê as três libs, reescreve os caminhos de asset relativos ao `home` do
    painel e devolve o payload único. Não escreve nada."""
    if active_tab not in ACTIVE_TABS:
        raise DashboardError(
            f"active_tab inválido: {active_tab!r} (use {', '.join(ACTIVE_TABS)}).")

    sdir, pdir, gdir = style_dir, product_dir, grid_dir
    if home is None:
        home = os.path.commonpath([str(sdir), str(pdir), str(gdir)])
    home = Path(home)

    style_pfx = _rel_prefix(Path(sdir), home)
    product_pfx = _rel_prefix(Path(pdir), home)

    # --- estilos (thumbnail relativo a style-gallery/) ---
    styles = []
    for s in sl.list_styles(lib_dir=sdir):
        s = dict(s)
        s["thumbnail"] = _reprefix(s.get("thumbnail"), style_pfx)
        styles.append(s)

    # --- catálogo (photos relativos a product-catalog/) ---
    brands = pl.list_brands(lib_dir=pdir)
    products = []
    for p in pl.list_products(lib_dir=pdir):
        p = dict(p)
        p["photos"] = [_reprefix(ph, product_pfx) for ph in (p.get("photos") or [])]
        products.append(p)

    # --- grids (mockup do dia relativo a grids/) ---
    grids = []
    for g in gl.list_grids_full(lib_dir=gdir):
        g = dict(g)
        new_weeks = []
        for w in g.get("weeks", []):
            w = dict(w)
            days = []
            for d in w.get("days", []):
                d = dict(d)
                if d.get("mockup"):
                    d["mockup"] = _resolve_grid_asset(d["mockup"], gdir, home)
                if d.get("video"):
                    d["video"] = _resolve_grid_asset(d["video"], gdir, home)
                days.append(d)
            w["days"] = days
            new_weeks.append(w)
        g["weeks"] = new_weeks
        grids.append(g)

    # --- meta.brands: união canônica (catálogo + marcas que só existem em grids) ---
    brand_names = {b.get("slug"): (b.get("name") or b.get("slug")) for b in brands}
    for g in grids:
        bslug = g.get("brand")
        if bslug and bslug not in brand_names:
            brand_names[bslug] = bslug
    meta_brands = [{"slug": k, "name": v} for k, v in sorted(brand_names.items())]

    return {
        "styles": styles,
        "catalog": {"brands": brands, "products": products},
        "grids": grids,
        "activeTab": active_tab,
        "meta": {"brands": meta_brands, "generatedAt": lc.now()},
    }


# --------------------------------------------------------------------------- #
# render / open
# --------------------------------------------------------------------------- #
def render_dashboard(*, active_tab="styles", out_dir=None,
                     style_dir=None, product_dir=None, grid_dir=None,
                     template_path=None) -> Path:
    """Materializa as três libs, compõe o payload, injeta no template único e
    escreve `<home>/insideout-painel.html`. `home` = raiz comum das três pastas
    (tipicamente a pasta de trabalho) ou `out_dir`, se dado. Devolve o caminho."""
    if active_tab not in ACTIVE_TABS:
        raise DashboardError(
            f"active_tab inválido: {active_tab!r} (use {', '.join(ACTIVE_TABS)}).")

    sdir, pdir, gdir = _ensure_all(style_dir, product_dir, grid_dir)
    home = Path(out_dir) if out_dir is not None else Path(
        os.path.commonpath([str(sdir), str(pdir), str(gdir)]))
    home.mkdir(parents=True, exist_ok=True)

    payload = build_payload(active_tab=active_tab,
                            style_dir=sdir, product_dir=pdir, grid_dir=gdir,
                            home=home)
    tpl = Path(template_path or _TEMPLATE_FILE).read_text(encoding="utf-8")
    injected = lc.inject_placeholder(
        tpl, _PLACEHOLDER, json.dumps(payload, ensure_ascii=False), DashboardError)
    html_path = home / _HTML_NAME
    lc.atomic_write(html_path, injected)
    return html_path


def open_dashboard(active_tab="styles", **kw) -> Path:
    """Regenera e devolve o caminho do painel (a skill instrui o usuário a abrir,
    com deep-link na aba via fragmento `#styles|#products|#grid`)."""
    return render_dashboard(active_tab=active_tab, **kw)

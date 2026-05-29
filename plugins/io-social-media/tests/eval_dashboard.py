"""
eval_dashboard — smoke determinístico do painel unificado (estilos×produtos×grid).

Roda 100% em diretório temporário (nunca na raiz do repo — fricção registrada),
sem rede e sem Gemini. Gera o painel a partir do seed das três libs e verifica:

  1. o arquivo `insideout-painel.html` é escrito e não-vazio;
  2. o placeholder foi substituído e o JSON injetado tem as 3 seções não-vazias
     (styles / catalog / grids), `activeTab` e `meta.brands` com 'clinique';
  3. o chassi não está duplicado — `function el(` aparece exatamente 1 vez;
  4. gate DOM-safe — sem `.innerHTML =` dinâmico e sem `.exec(` (usa matchAll);
  5. os caminhos de asset foram reescritos relativos à raiz do painel
     (`style-gallery/...`, `product-catalog/...`) e os arquivos EXISTEM no disco
     (materialização das 3 libs — não há asset mudo/quebrado).

Uso: `python eval_dashboard.py`. Exit 0 se tudo verde, 1 caso contrário.
Sem CI no repo — rodar manual antes do bump.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_CORE = _HERE.parent / "core"
sys.path.insert(0, str(_CORE))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import dashboard  # noqa: E402


def _extract_payload(html: str) -> dict:
    """Extrai o JSON injetado de `const data = <JSON> || {};`."""
    m = re.search(r"const data = (.*?) \|\| \{\};", html, re.DOTALL)
    if not m:
        raise AssertionError("não achei o payload injetado no template")
    return json.loads(m.group(1))


def main() -> int:
    fails: list[str] = []

    def check(cond: bool, msg: str):
        mark = "OK  " if cond else "FALHA"
        print(f"  [{mark}] {msg}")
        if not cond:
            fails.append(msg)

    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        sdir = home / "style-gallery"
        pdir = home / "product-catalog"
        gdir = home / "grids"

        path = dashboard.render_dashboard(
            active_tab="grid",
            style_dir=sdir, product_dir=pdir, grid_dir=gdir, out_dir=home)

        print("Painel gerado em:", path)
        check(path.exists() and path.name == "insideout-painel.html",
              "arquivo insideout-painel.html escrito na raiz comum")
        html = path.read_text(encoding="utf-8")
        check(len(html) > 5000, "HTML não-vazio")

        # (2) payload
        check(dashboard._PLACEHOLDER not in html, "placeholder substituído")
        payload = _extract_payload(html)
        check(len(payload.get("styles", [])) > 0, "seção styles não-vazia (seed)")
        check(len(payload.get("catalog", {}).get("brands", [])) > 0,
              "seção catalog.brands não-vazia (seed)")
        check(len(payload.get("catalog", {}).get("products", [])) > 0,
              "seção catalog.products não-vazia (seed)")
        check(len(payload.get("grids", [])) > 0, "seção grids não-vazia (seed)")
        check(payload.get("activeTab") == "grid", "activeTab == grid")
        brand_slugs = [b.get("slug") for b in payload.get("meta", {}).get("brands", [])]
        check("clinique" in brand_slugs, f"meta.brands contém clinique ({brand_slugs})")

        # (3) chassi único
        n_el = len(re.findall(r"function el\(", html))
        check(n_el == 1, f"function el( aparece exatamente 1x (achei {n_el})")
        for sec in ("tab-styles", "tab-products", "tab-grid"):
            check(f'id="{sec}"' in html, f'seção id="{sec}" presente')

        # (4) gate DOM-safe
        check(".innerHTML" not in html, "sem .innerHTML (DOM-safe)")
        check(".exec(" not in html, "sem .exec( (usa matchAll)")

        # (5) assets reescritos + existentes no disco
        st0 = payload["styles"][0]
        thumb = st0.get("thumbnail", "")
        check(thumb.startswith("style-gallery/"),
              f"thumbnail reescrito p/ style-gallery/ ({thumb})")
        check((home / thumb).exists(), f"thumbnail existe no disco ({thumb})")

        prod_with_photo = next(
            (p for p in payload["catalog"]["products"] if p.get("photos")), None)
        check(prod_with_photo is not None, "há ao menos 1 produto com foto no seed")
        if prod_with_photo:
            photo = prod_with_photo["photos"][0]
            check(photo.startswith("product-catalog/"),
                  f"foto reescrita p/ product-catalog/ ({photo})")
            check((home / photo).exists(), f"foto existe no disco ({photo})")

        # materialização das 3 libs
        for d in (sdir, pdir, gdir):
            check(d.is_dir(), f"pasta materializada: {d.name}/")

    print()
    if fails:
        print(f"RESULTADO: {len(fails)} falha(s) ❌")
        return 1
    print("RESULTADO: tudo verde ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

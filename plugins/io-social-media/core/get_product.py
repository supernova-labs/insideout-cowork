"""
get_product.py — shim fino de back-compat sobre product_library.

Contrato CLI (consumido pela skill `image-generation` na junção estilo×produto):
  python get_product.py --list                 lista marcas e produtos
  python get_product.py --brand <slug|nome|id> lista produtos de uma marca
  python get_product.py <id|slug|nome>         resolve 1 produto (full)

A lógica real (resolução workspace/seed, fotos, brief da marca) vive em
product_library.py. Este arquivo só formata a saída CLI e expõe
get_product()/list_products() para quem importa por compatibilidade.
"""
import sys
from pathlib import Path

# Windows: console é cp1252 por padrão e quebra com emoji/acentos.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# .parent SEM .resolve(): mesma disciplina do _libcommon — .resolve() segue a
# junção UWP/MSIX e devolve caminho não-stat-ável (aqui quebraria o import).
sys.path.insert(0, str(Path(__file__).parent))

from product_library import (  # noqa: E402
    get_product_resolved as _get_product,
    list_brands as _list_brands,
    list_products as _list_products,
    ProductCatalogError,
)


def get_product(ref, brand=None):
    """Back-compat: produto + brief da marca + fotos absolutas."""
    return _get_product(ref, brand)


def list_products(brand=None):
    """Back-compat: lista [{id, slug, name, brand}, ...]."""
    return [{"id": p.get("id"), "slug": p.get("slug"),
             "name": p.get("name"), "brand": p.get("brand")}
            for p in _list_products(brand)]


def _print_full(prod):
    brief = prod.get("_brand_brief") or {}
    print(f"Produto #{prod.get('id')}: {prod.get('name')}  "
          f"[{prod.get('slug')}]")
    print(f"Marca: {brief.get('name', prod.get('brand', 'N/A'))}")
    if prod.get("description"):
        print(f"Descrição: {prod['description']}")
    if prod.get("claims"):
        print(f"Claims: {', '.join(prod['claims'])}")
    if prod.get("tags"):
        print(f"Tags: {', '.join(prod['tags'])}")
    photos = prod.get("_photos_abs", [])
    print(f"\nFotos ({len(photos)}):")
    for ph in photos:
        print(f"  {ph}")
    if brief:
        print("\n-- Brief da marca --")
        print(f"Voz: {brief.get('voice', 'N/A')}")
        if brief.get("keyMessages"):
            print("Mensagens-chave:")
            for m in brief["keyMessages"]:
                print(f"  - {m}")
        print(f"Público: {brief.get('audience', 'N/A')}")
        if brief.get("paletteHints"):
            print(f"Paleta: {brief['paletteHints']}")
        if brief.get("guardrails"):
            print(f"Guardrails: {brief['guardrails']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_product.py <id|slug|nome>")
        print("       python get_product.py --brand <slug|nome|id>")
        print("       python get_product.py --list")
        sys.exit(1)

    if sys.argv[1] == "--list":
        brands = _list_brands()
        products = _list_products()
        print(f"Marcas ({len(brands)}):")
        for b in brands:
            n = len([p for p in products if p.get("brand") == b.get("slug")])
            print(f"  {b.get('slug')}: {b.get('name')} ({n} produto(s))")
        print(f"\nProdutos ({len(products)}):")
        for p in products:
            print(f"  #{p.get('id', 0):2d} [{p.get('brand')}] "
                  f"{p.get('name')} ({p.get('slug')})")
    elif sys.argv[1] == "--brand":
        if len(sys.argv) < 3:
            print("Usage: python get_product.py --brand <slug|nome|id>")
            sys.exit(1)
        try:
            prods = _list_products(sys.argv[2])
        except ProductCatalogError as e:
            print(f"Error: {e}")
            sys.exit(1)
        print(f"Produtos da marca '{sys.argv[2]}' ({len(prods)}):")
        for p in prods:
            print(f"  #{p.get('id', 0):2d} {p.get('name')} ({p.get('slug')})")
    else:
        try:
            prod = _get_product(sys.argv[1])
        except ProductCatalogError as e:
            print(f"Error: {e}")
            sys.exit(1)
        _print_full(prod)

"""
get_grid.py — shim fino de back-compat sobre grid_library.

Contrato CLI (consumido pela skill `generate-grid`):
  python get_grid.py --list                 lista todos os grids (marca/mês)
  python get_grid.py --brand <slug|nome>    lista grids de uma marca
  python get_grid.py <marca> <AAAA-MM>      imprime 1 grid (resumo + dias)

A lógica real (resolução workspace/seed, ingestão, ops de post, render) vive
em grid_library.py. Este arquivo só formata a saída CLI e expõe
get_grid()/list_grids() para quem importa por compatibilidade.
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

from grid_library import (  # noqa: E402
    get_grid as _get_grid,
    list_grids as _list_grids,
    GridError,
)


def get_grid(brand, month):
    """Back-compat: grid canônico completo de uma marca-mês."""
    return _get_grid(brand, month)


def list_grids(brand=None):
    """Back-compat: lista [{brand, month, focusProducts, posts}, ...]."""
    return _list_grids(brand)


def _print_grid(g):
    print(f"Grid: {g.get('brand')} / {g.get('month')}")
    fp = g.get("focusProducts") or []
    if fp:
        print(f"Produtos-foco: {', '.join(fp)}")
    if g.get("ingestedFrom"):
        src = g["ingestedFrom"]
        print(f"Ingerido de: {src.get('file')} ({src.get('sheet')})")
    for w in g.get("weeks", []):
        print(f"\n-- Semana {w.get('n')} --")
        for d in w.get("days", []):
            bits = [d.get("date"), d.get("dow")]
            if d.get("channel"):
                bits.append(f"[{d['channel']}]")
            if d.get("approach"):
                bits.append(d["approach"])
            subj = d.get("subject") or d.get("product") or "—"
            line = "  " + " ".join(str(b) for b in bits) + f"  {subj}"
            print(line)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_grid.py <marca> <AAAA-MM>")
        print("       python get_grid.py --brand <slug|nome>")
        print("       python get_grid.py --list")
        sys.exit(1)

    if sys.argv[1] == "--list":
        grids = _list_grids()
        print(f"Grids ({len(grids)}):")
        for g in grids:
            print(f"  {g.get('brand')}/{g.get('month')} "
                  f"({g.get('posts', 0)} post(s))")
    elif sys.argv[1] == "--brand":
        if len(sys.argv) < 3:
            print("Usage: python get_grid.py --brand <slug|nome>")
            sys.exit(1)
        try:
            grids = _list_grids(sys.argv[2])
        except GridError as e:
            print(f"Error: {e}")
            sys.exit(1)
        print(f"Grids da marca '{sys.argv[2]}' ({len(grids)}):")
        for g in grids:
            print(f"  {g.get('month')} ({g.get('posts', 0)} post(s))")
    else:
        if len(sys.argv) < 3:
            print("Usage: python get_grid.py <marca> <AAAA-MM>")
            sys.exit(1)
        try:
            g = _get_grid(sys.argv[1], sys.argv[2])
        except GridError as e:
            print(f"Error: {e}")
            sys.exit(1)
        _print_grid(g)

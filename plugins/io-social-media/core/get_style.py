"""
get_style.py — shim fino de back-compat sobre style_library.

Mantém o contrato histórico ("estilo #N") usado por skills/usuários da 0.2.x:
  python get_style.py <id|slug>
  python get_style.py --list

A lógica real (resolução workspace/seed, formato dos dados) vive em
style_library.py. Este arquivo só formata a saída CLI e expõe
get_style()/list_styles() para quem importa por compatibilidade.
"""
import sys
from pathlib import Path

# Windows: console é cp1252 por padrão e quebra com emoji/acentos nos prompts.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))

from style_library import (  # noqa: E402
    get_style as _get_style,
    list_styles as _list_styles,
    StyleLibraryError,
)


def get_style(style_id):
    """Back-compat: aceita id (int) ou slug (str). Retorna o dict do estilo."""
    return _get_style(style_id)


def list_styles():
    """Back-compat: lista [{id, name}, ...]."""
    return [{"id": s.get("id"), "name": s.get("name")} for s in _list_styles()]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_style.py <id|slug>")
        print("       python get_style.py --list")
        sys.exit(1)

    if sys.argv[1] == "--list":
        styles = _list_styles()
        print(f"Available styles ({len(styles)} total):\n")
        for s in styles:
            print(f"  #{s.get('id', 0):2d}: {s.get('name', '')}")
    else:
        try:
            style = _get_style(sys.argv[1])
        except StyleLibraryError as e:
            print(f"Error: {e}")
            sys.exit(1)
        print(f"Style #{style['id']}: {style['name']}")
        print(f"Category: {style.get('category', 'N/A')}")
        print(f"Example use: {style.get('exampleUse', 'N/A')}")
        print(f"\nPrompt:\n{style['prompt']}")

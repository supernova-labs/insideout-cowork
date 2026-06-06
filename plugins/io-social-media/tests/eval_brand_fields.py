"""
eval_brand_fields — smoke dos campos de marca do PR 0.13.0 (E2/E3) e do escopo (E1).

Roda 100% em diretório temporário (nunca na raiz do repo). Verifica:

  E3  — a marca do seed (Clinique) tem `positioning` preenchido; `add_brand`
        aceita `positioning`.
  E2  — a marca tem `brandGuide` com a identidade visual (Clinique Green/#C5D6B8);
        `add_brand` aceita `brand_guide`; e `compose_generation_brief` INJETA
        positioning + brandGuide no prompt (o payoff: a geração usa).
  E1  — o escopo contratado da Clinique existe e é legível, com "Dentro do escopo"
        e "Fora do escopo" (red flags) + a cota de telas.

Uso: `python eval_brand_fields.py`. Exit 0 se tudo verde, 1 caso contrário.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_CORE = _HERE.parent / "core"
_SCOPE = _HERE.parent / "skills" / "analyze-briefing" / "scopes" / "clinique.md"
sys.path.insert(0, str(_CORE))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import product_library as pc  # noqa: E402

_fail = []


def check(cond, label):
    print(f"  [{'OK  ' if cond else 'FALHA'}] {label}")
    if not cond:
        _fail.append(label)


def main():
    ws = tempfile.mkdtemp(prefix="io_brand_")
    os.chdir(ws)

    # seed parseia com os campos novos
    seed = json.load(open(_CORE / "products.seed.json", encoding="utf-8"))
    check(seed["brands"][0]["slug"] == "clinique", "seed parseia e tem marca clinique")

    b = pc.get_brand("clinique")
    check(bool(b.get("positioning", "").strip()), "E3 marca tem positioning")
    bg = b.get("brandGuide", "")
    check("Clinique Green" in bg and "#C5D6B8" in bg, "E2 brandGuide tem identidade visual (cor)")

    # compose injeta os dois no prompt
    prod = pc.get_product_resolved("almost-lipstick-black-honey")
    style = {"id": 1, "name": "Still life clean", "prompt": "fundo neutro, luz difusa"}
    p = pc.compose_generation_brief(style, prod, mode="preservar")["prompt"]
    check("Posicionamento" in p and "#C5D6B8" in p and "Produto é herói" in p,
          "E2/E3 compose_generation_brief injeta positioning + brandGuide")

    # add_brand aceita os campos novos
    nb = pc.add_brand("Marca Teste", positioning="posic", brand_guide="guide #FFF")
    check(nb.get("positioning") == "posic" and nb.get("brandGuide") == "guide #FFF",
          "E2/E3 add_brand aceita positioning/brand_guide")

    # E1 escopo legível
    txt = _SCOPE.read_text(encoding="utf-8")
    check("Dentro do escopo" in txt and "Fora do escopo" in txt and "90 telas" in txt,
          "E1 escopo Clinique legível (dentro/fora + cota)")

    os.chdir(tempfile.gettempdir())
    import shutil
    shutil.rmtree(ws, ignore_errors=True)

    print("\nRESULTADO:", "tudo verde ✅" if not _fail else f"FALHAS: {_fail}")
    sys.exit(1 if _fail else 0)


if __name__ == "__main__":
    main()

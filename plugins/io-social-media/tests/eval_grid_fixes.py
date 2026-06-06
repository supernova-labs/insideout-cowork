"""
eval_grid_fixes — smoke determinístico dos fixes de demo (0.12.0): campo `copy`
no grid (A2), normalização do caminho de mockup (A3) e guard de mojibake (A4).

Roda 100% em diretório temporário (nunca na raiz do repo — fricção registrada),
sem rede e sem Gemini. Cria um mês completo via `new_grid` (não depende da
cobertura do grid-seed) e verifica:

  A2  — `_empty_day` tem `copy`; `set_post(copy=...)` persiste com acento.
  A4  — `set_post` recusa texto com U+FFFD (mojibake) sem gravar.
  A3  — `attach_mockup` copia a imagem pro caminho canônico e grava o relativo;
        o painel resolve o mockup pra `grids/mockups/...` (canônico), NÃO duplica
        `grids/grids/...` quando o caminho vem como `grids/...`, e cai no
        fallback (prefixo cego) quando o arquivo ainda não existe.

Uso: `python eval_grid_fixes.py`. Exit 0 se tudo verde, 1 caso contrário.
Sem CI no repo — rodar manual antes do bump.
"""
from __future__ import annotations

import os
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

import grid_library as gl  # noqa: E402
import dashboard as dash    # noqa: E402

BRAND, MONTH, DAY, DAY2 = "clinique", "2026-07", "2026-07-10", "2026-07-11"
COPY = "Sua rotina Clinique não fica em casa: hidratação à prova de inverno — açaí, ênfase, coração."

_fail = []


def check(cond, label):
    print(f"  [{'OK  ' if cond else 'FALHA'}] {label}")
    if not cond:
        _fail.append(label)


def _mockup_of(payload, date):
    for g in payload["grids"]:
        if g["brand"] == BRAND and g["month"] == MONTH:
            for w in g["weeks"]:
                for d in w["days"]:
                    if d["date"] == date:
                        return d.get("mockup")
    return None


def main():
    ws = tempfile.mkdtemp(prefix="io_gridfix_")
    os.chdir(ws)

    gl.new_grid(BRAND, MONTH)  # mês completo, independente do seed

    # --- A2 ---
    ed = gl._empty_day("2026-05-15")
    check(ed.get("copy") == "", "A2 _empty_day tem campo copy vazio")
    gl.set_post(BRAND, MONTH, DAY, copy=COPY)
    day = gl._find_day(gl.get_grid(BRAND, MONTH), DAY)
    check(day.get("copy") == COPY, "A2 copy persiste com acento intacto")

    # --- A4 ---
    raised = False
    try:
        gl.set_post(BRAND, MONTH, DAY, copy="texto com � corrompido")
    except gl.InvalidGrid:
        raised = True
    check(raised, "A4 guard recusa U+FFFD (mojibake)")
    day = gl._find_day(gl.get_grid(BRAND, MONTH), DAY)
    check(day.get("copy") == COPY, "A4 copy boa não foi sobrescrita pela recusa")

    # --- A3: attach_mockup canônico ---
    dummy = os.path.join(ws, "ad_hoc.png")
    with open(dummy, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"0" * 64)
    r = gl.attach_mockup(BRAND, MONTH, DAY, dummy)
    check(r["mockup"] == f"mockups/{MONTH}/{DAY}.png", "A3 attach_mockup grava rel canônico")
    check(os.path.isfile(r["absolute_path"]), "A3 attach_mockup copia o arquivo")

    sdir, pdir, gdir = dash._ensure_all()
    payload = dash.build_payload(active_tab="grid", style_dir=sdir, product_dir=pdir, grid_dir=gdir)
    check(_mockup_of(payload, DAY) == f"grids/mockups/{MONTH}/{DAY}.png",
          "A3 painel resolve mockup canônico p/ grids/mockups/...")

    # --- A3: caminho 'grids/...' não duplica em 'grids/grids/...' ---
    gl.set_post(BRAND, MONTH, DAY, mockup=f"grids/mockups/{MONTH}/{DAY}.png")
    sdir, pdir, gdir = dash._ensure_all()
    payload = dash.build_payload(active_tab="grid", style_dir=sdir, product_dir=pdir, grid_dir=gdir)
    m = _mockup_of(payload, DAY)
    check(m == f"grids/mockups/{MONTH}/{DAY}.png" and "grids/grids" not in (m or ""),
          "A3 sem duplicação 'grids/grids' quando o caminho vem da raiz")

    # --- A3: fallback quando o arquivo ainda não existe ---
    gl.set_post(BRAND, MONTH, DAY2, mockup=f"mockups/{MONTH}/{DAY2}.png")
    sdir, pdir, gdir = dash._ensure_all()
    payload = dash.build_payload(active_tab="grid", style_dir=sdir, product_dir=pdir, grid_dir=gdir)
    check(_mockup_of(payload, DAY2) == f"grids/mockups/{MONTH}/{DAY2}.png",
          "A3 fallback (prefixo cego) p/ arquivo ainda inexistente")

    # --- Vídeo no grid (0.14.0): campo video + attach_video + resolução ---
    DAY3 = "2026-07-12"
    check(gl._empty_day("2026-07-20").get("video") is None,
          "vídeo: _empty_day tem campo video (None)")
    vmp4 = os.path.join(ws, "ad.mp4")
    with open(vmp4, "wb") as f:
        f.write(b"\x00\x00\x00\x18ftypmp42" + b"0" * 64)
    rv = gl.attach_video(BRAND, MONTH, DAY3, vmp4)
    check(rv["video"] == f"mockups/{MONTH}/{DAY3}.mp4" and os.path.isfile(rv["absolute_path"]),
          "vídeo: attach_video grava rel canônico + copia o arquivo")
    sdir, pdir, gdir = dash._ensure_all()
    payload = dash.build_payload(active_tab="grid", style_dir=sdir, product_dir=pdir, grid_dir=gdir)

    def _video_of(p, date):
        for g in p["grids"]:
            if g["brand"] == BRAND and g["month"] == MONTH:
                for w in g["weeks"]:
                    for d in w["days"]:
                        if d["date"] == date:
                            return d.get("video")
        return None
    check(_video_of(payload, DAY3) == f"grids/mockups/{MONTH}/{DAY3}.mp4",
          "vídeo: painel resolve o video p/ grids/mockups/...mp4")

    os.chdir(tempfile.gettempdir())
    import shutil
    shutil.rmtree(ws, ignore_errors=True)

    print("\nRESULTADO:", "tudo verde ✅" if not _fail else f"FALHAS: {_fail}")
    sys.exit(1 if _fail else 0)


if __name__ == "__main__":
    main()

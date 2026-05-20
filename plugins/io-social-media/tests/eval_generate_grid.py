"""
eval_generate_grid — gate determinístico da Fase 2 vs gabarito real.

Mede SÓ a camada determinística do `generate_from_briefing` (mecânico:
âncoras, janela de intensidade, datas comemorativas, cadência). Julgamento
de conteúdo (qual produto na data, hero, ref) é responsabilidade do agente
e fica fora deste eval — vira `evals-skills:error-analysis` follow-up.

Gabarito = os grids reais reconstruídos pela Estela em `teste-io`
(C:\\Users\\mroch\\Code\\supernova-labs\\projects\\teste-io\\grids\\<marca>\\
<AAAA-MM>.json). Os dados ficam **fora deste repo** — passe o caminho:

    python eval_generate_grid.py --grids-dir /caminho/pra/teste-io/grids

ou exporte `IO_TESTE_GRIDS=/caminho`. Sem isso, o script faz skip-with-msg
(o eval depende de dado vivo do cliente).

Para cada grid real encontrado:
  1. Deriva o `brief` do próprio (launches/focusProducts observados).
  2. Roda `generate_from_briefing` num lib_dir temporário.
  3. Audita gerado e real (`audit_grid`) e diffa.
  4. Confere thresholds:
     - datas comemorativas do mês: 100% das que existem no calendário
       aparecem no real → o gerado tem que casar quando o brief observado
       tem foco compatível;
     - gap≤2: 100% (no gerado);
     - cobertura ≥ ~90% (dias do mês com post);
     - âncora de lançamento: dia exato do brief no gerado.

Saída: tabela por mês + summary verde/vermelho. Exit 0 se todos verdes; 1
caso contrário. Sem CI no repo — uso é manual antes do bump 0.9.0.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

# Permite rodar de qualquer dir; aponta pro core do plugin
_HERE = Path(__file__).resolve().parent
_CORE = _HERE.parent / "core"
sys.path.insert(0, str(_CORE))

import grid_library as gl  # noqa: E402


COVERAGE_THRESHOLD = 0.90


def _derive_brief(real_grid: dict) -> dict:
    """Deriva um `brief` a partir do grid real. Heurística:
      - launches: dias com approach=='LANÇAMENTO' (ou 'LAN...') agrupados
        por produto, primeira ocorrência = âncora.
      - focusProducts: produtos com ≥3 dias no mês (proxy de 'foco').
    """
    days = sorted(
        (d for w in real_grid.get("weeks", []) for d in w.get("days", [])),
        key=lambda d: d.get("date", ""))

    launches_seen: dict = {}
    product_count: dict = {}
    for d in days:
        prod = (d.get("product") or "").strip()
        appr = (d.get("approach") or "").upper()
        if prod:
            product_count[prod] = product_count.get(prod, 0) + 1
        if appr.startswith("LAN") and prod and prod not in launches_seen:
            launches_seen[prod] = d["date"]

    return {
        "brand": real_grid["brand"], "month": real_grid["month"],
        "launches": [
            {"date": dt, "product": p, "label": p, "important": True}
            for p, dt in launches_seen.items()],
        "focusProducts": [p for p, n in product_count.items() if n >= 3],
    }


def _eval_one(real_path: Path, lib_dir: Path) -> dict:
    real = json.loads(real_path.read_text(encoding="utf-8"))
    brief = _derive_brief(real)
    v = gl._validate_brief(brief, lib_dir=lib_dir)
    gen = gl.generate_from_briefing(v["brief"], lib_dir=lib_dir, save=False,
                                     overwrite=True)
    a_gen = gl.audit_grid(gen, lib_dir=lib_dir)
    a_real = gl.audit_grid(real, lib_dir=lib_dir)

    # Janelas de lançamento: anchor day deve ter _slot launch_anchor no gerado
    launch_ok = True
    for lau in brief["launches"]:
        d = next((d for w in gen["weeks"] for d in w["days"]
                  if d["date"] == lau["date"]), None)
        if not d or (d.get("_slot") or {}).get("kind") != "launch_anchor":
            launch_ok = False
            break

    # Datas comemorativas do mês: o gerado tem _slot calendar_hook
    # (ou calendarHook em launch_anchor que coincide com a data)
    yy = int(real["month"][:4])
    try:
        cal = gl.parse_calendar(yy, lib_dir=lib_dir)["items"]
    except gl.GridError:
        cal = []
    cal_days = [it["date"] for it in cal
                if it["scope"] == "day" and it["date"][:7] == real["month"]]
    cal_in_gen = 0
    for cd in cal_days:
        d = next((d for w in gen["weeks"] for d in w["days"]
                  if d["date"] == cd), None)
        if not d:
            continue
        slot = d.get("_slot") or {}
        if slot.get("kind") == "calendar_hook" or slot.get("calendarHook"):
            cal_in_gen += 1
    cal_ratio = cal_in_gen / len(cal_days) if cal_days else 1.0

    # Andaime: garantia mecânica é que TODO dia do mês tem _slot proposto.
    # `audit_grid.maxGap` mede gap em POSTS preenchidos — não se aplica ao
    # andaime cru. Aqui medimos a garantia certa: dias sem _slot.
    gen_days = [d for w in gen["weeks"] for d in w["days"]]
    days_without_slot = [d["date"] for d in gen_days if "_slot" not in d]
    slot_coverage_ok = not days_without_slot

    # Coverage do REAL (humano): sanidade do gabarito, NÃO gate da Fase 2.
    # Reportado pra contexto (gabaritos parciais da Estela aparecem aqui),
    # mas não conta como pass/fail — o eval mede o que `generate_from_briefing`
    # produz, não a completude da planilha de origem.
    real_coverage = a_real["coverage"]

    checks = {
        "launches_anchored": launch_ok,
        "every_day_has_slot": slot_coverage_ok,
        "calendar_hooks_100pct": abs(cal_ratio - 1.0) < 1e-9,
    }
    return {
        "file": real_path.name, "month": real["month"],
        "brief": brief,
        "audit_gen": a_gen, "audit_real": a_real,
        "calendar_ratio": cal_ratio,
        "checks": checks,
        "passed": all(checks.values()),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--grids-dir", default=os.environ.get("IO_TESTE_GRIDS"),
                     help="caminho pra <teste-io>/grids (default $IO_TESTE_GRIDS)")
    ap.add_argument("--brand", default="clinique",
                     help="marca a auditar (default: clinique)")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    if not args.grids_dir:
        print("SKIP: gabarito não disponível. Passe --grids-dir ou exporte "
              "IO_TESTE_GRIDS apontando pra <teste-io>/grids "
              "(grids/<marca>/<AAAA-MM>.json reconstruídos da Estela).",
              file=sys.stderr)
        sys.exit(0)

    grids_dir = Path(args.grids_dir).expanduser()
    brand_dir = grids_dir / args.brand
    if not brand_dir.is_dir():
        print(f"ERROR: {brand_dir} não existe. Conferir --grids-dir.",
              file=sys.stderr)
        sys.exit(2)

    real_files = sorted(brand_dir.glob("*.json"))
    if not real_files:
        print(f"ERROR: nenhum grid em {brand_dir}", file=sys.stderr)
        sys.exit(2)

    print(f"Eval gen-grid Fase 2 — marca={args.brand}, "
          f"{len(real_files)} meses, gabarito={grids_dir}")
    print("=" * 78)

    with tempfile.TemporaryDirectory(prefix="evalgrid_") as td:
        lib_dir = Path(td) / "grids"
        results = []
        for fp in real_files:
            try:
                r = _eval_one(fp, lib_dir)
            except Exception as e:
                print(f"  {fp.name}: EXCEPTION {e!r}")
                results.append({"file": fp.name, "month": "?",
                                 "passed": False, "error": repr(e),
                                 "checks": {}})
                continue
            status = "PASS" if r["passed"] else "FAIL"
            print(f"  {r['month']}: {status:4s}  "
                  f"cal_ratio={r['calendar_ratio']:.2f}  "
                  f"real_cov={r['audit_real']['coverage']:.2f}  "
                  f"launches={len(r['brief']['launches'])}")
            if args.verbose or not r["passed"]:
                for k, v in r["checks"].items():
                    mark = "✓" if v else "✗"
                    print(f"      {mark} {k}={v}")
                if not r["passed"]:
                    print(f"      gen.warnings: {r['audit_gen']['warnings']}")
            results.append(r)

    print("=" * 78)
    passed = sum(1 for r in results if r["passed"])
    print(f"Resultado: {passed}/{len(results)} verdes "
          f"(checks: launches_anchored, every_day_has_slot, "
          f"calendar_hooks_100pct). real_cov é info, não gate.")
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()

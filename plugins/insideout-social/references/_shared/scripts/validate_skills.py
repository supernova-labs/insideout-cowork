#!/usr/bin/env python3
"""Validação estrutural determinística do plugin Codex InsideOut Social."""
from __future__ import annotations

import json
import re
from pathlib import Path


SHARED_ROOT = Path(__file__).parent.parent
ROOT = SHARED_ROOT.parent.parent / "skills"
PLUGIN_MANIFEST = ROOT.parent / ".codex-plugin" / "plugin.json"
SKILLS = {
    "analyze-briefing": ROOT / "analyze-briefing",
    "generate-copy": ROOT / "generate-copy",
    "generate-grid": ROOT / "generate-grid",
    "generate-image": ROOT / "generate-image",
    "generate-video": ROOT / "generate-video",
}
REQUIRED_SHARED = (
    SHARED_ROOT / "voz-usuario.md",
    SHARED_ROOT / "about-insideout.md",
    SHARED_ROOT / "airtable-contract.md",
    SHARED_ROOT / "evals" / "resposta-sem-ids.md",
)
FORBIDDEN = (
    "${CLAUDE_PLUGIN_ROOT}",
    "grid_library",
    "product_library",
    "insideout-painel.html",
    "GEMINI_API_KEY",
)
HARDCODED_AIRTABLE_ID = re.compile(r"\b(?:app|tbl|fld)[A-Za-z0-9]{14,}\b")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    out: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip().strip("'\"")
    return out


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for path in REQUIRED_SHARED:
        if not path.is_file():
            errors.append(f"arquivo compartilhado ausente: {path.relative_to(ROOT)}")

    for name, skill_dir in SKILLS.items():
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{name}: SKILL.md ausente")
            continue
        text = skill_file.read_text(encoding="utf-8")
        meta = frontmatter(text)
        if meta.get("name") != name:
            errors.append(f"{name}: frontmatter name divergente")
        if not meta.get("description"):
            errors.append(f"{name}: description ausente")
        lines = text.count("\n") + 1
        if lines >= 500:
            errors.append(f"{name}: SKILL.md tem {lines} linhas (limite <500)")
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"{name}: dependência legada encontrada: {token}")
        if HARDCODED_AIRTABLE_ID.search(text):
            errors.append(f"{name}: ID do Airtable hardcoded no SKILL.md")

        eval_dir = skill_dir / "evals"
        evals = sorted(eval_dir.glob("*.md")) if eval_dir.is_dir() else []
        if len(evals) < 3:
            errors.append(f"{name}: menos de 3 evals versionados")
        for eval_file in evals:
            eval_text = eval_file.read_text(encoding="utf-8")
            for heading in ("## Prompt", "## Resultado esperado"):
                if heading not in eval_text:
                    errors.append(
                        f"{eval_file.relative_to(ROOT)}: seção {heading!r} ausente"
                    )

    if not PLUGIN_MANIFEST.is_file():
        errors.append("manifesto Codex ausente: .codex-plugin/plugin.json")
    else:
        try:
            manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"manifesto Codex inválido: {exc.msg}")
        else:
            if manifest.get("name") != "insideout-social":
                errors.append("manifesto Codex: name deve ser insideout-social")
            if not manifest.get("version"):
                errors.append("manifesto Codex: version ausente")
            if manifest.get("skills") != "./skills/":
                errors.append("manifesto Codex: skills deve apontar para ./skills/")

    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "skills": sorted(SKILLS),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

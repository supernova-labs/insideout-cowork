#!/usr/bin/env python3
"""Validate the distributable Hyundai skill graph; no operational writes."""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "insideout-hyundai-social"
EXPECTED = {"research-month", "generate-grid", "review-grid-feedback", "send-to-asana"}


def validate() -> list[str]:
    errors = []
    paths = list((PLUGIN / "skills").glob("*/SKILL.md"))
    if {p.parent.name for p in paths} != EXPECTED:
        errors.append("The package must expose exactly the four Hyundai skills")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        meta = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", text)
        if not meta or meta[1] != path.parent.name:
            errors.append(f"Invalid frontmatter: {path.relative_to(REPO)}")
        if len(text.splitlines()) >= 500:
            errors.append(f"Skill exceeds the line limit: {path.parent.name}")
        ui = path.parent / "agents" / "openai.yaml"
        if not ui.is_file() or f"${path.parent.name}" not in ui.read_text(encoding="utf-8"):
            errors.append(f"Missing invocation metadata: {path.parent.name}")
        evals = list((path.parent / "evals").glob("*.md"))
        if len(evals) < 3:
            errors.append(f"Missing regression scenarios: {path.parent.name}")
        for case in evals:
            content = case.read_text(encoding="utf-8")
            if "## Prompt" not in content or "## Resultado esperado" not in content:
                errors.append(f"Incomplete eval: {case.relative_to(REPO)}")

    for path in PLUGIN.rglob("*"):
        if path.is_symlink():
            errors.append(f"Unexpected symlink: {path.relative_to(REPO)}")
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".json", ".yaml"}:
            errors.append(f"Runtime/operational asset in package: {path.relative_to(REPO)}")
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"\b(?:app|tbl|fld|rec)[A-Za-z0-9]{14}\b", text):
            errors.append(f"Hardcoded operational identity: {path.relative_to(REPO)}")
        # Check each literal file dependency, including shared references.
        for target in re.findall(r"`([^`\n]+\.md)`", text):
            if " " in target or "<" in target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(PLUGIN) or not resolved.is_file():
                errors.append(f"Broken/escaping reference: {path.relative_to(REPO)} -> {target}")

    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if manifest["name"] != PLUGIN.name or manifest["skills"] != "./skills/":
        errors.append("Plugin manifest does not resolve to the canonical skill tree")
    if manifest.get("apps") != "./.app.json":
        errors.append("Plugin must declare its Airtable app mapping")
    app_path = PLUGIN / ".app.json"
    if not app_path.is_file():
        errors.append("Missing Airtable app mapping")
    else:
        apps = json.loads(app_path.read_text(encoding="utf-8")).get("apps", {})
        if apps != {"airtable": {"id": "asdk_app_693ca6ce2db08191bb52d66743c65184", "required": True}}:
            errors.append("App mapping must require the official Airtable connector only")
    if len(manifest.get("interface", {}).get("defaultPrompt", [])) > 3:
        errors.append("Too many marketplace prompts")
    catalog = json.loads((REPO / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    matches = [p for p in catalog["plugins"] if p["name"] == PLUGIN.name]
    if len(matches) != 1 or matches[0]["source"]["path"] != "./plugins/" + PLUGIN.name:
        errors.append("Catalog does not point uniquely to the plugin")
    elif matches[0].get("policy", {}).get("authentication") != "ON_INSTALL":
        errors.append("Catalog must request Airtable authentication on install")
    index = json.loads((REPO / ".agent-smith" / "index.json").read_text(encoding="utf-8"))
    components = [c for c in index["components"] if c.get("plugin") == PLUGIN.name and c["type"] == "skill"]
    if {c["name"] for c in components} != EXPECTED or len(components) != len(EXPECTED):
        errors.append("Architecture inventory diverges from the filesystem")
    for component in components:
        adapters = [a for a in index["adapters"] if a["componentId"] == component["id"]]
        if len(adapters) != 1 or adapters[0]["path"] != component["canonicalPath"]:
            errors.append(f"Adapter mismatch: {component['name']}")
    app_components = [c for c in index["components"] if c["id"] == "mcp:insideout-hyundai-social:airtable"]
    app_adapters = [a for a in index["adapters"] if a["componentId"] == "mcp:insideout-hyundai-social:airtable"]
    app_relative = "plugins/insideout-hyundai-social/.app.json"
    if len(app_components) != 1 or app_components[0]["canonicalPath"] != app_relative:
        errors.append("Missing Airtable mapping in architecture inventory")
    if len(app_adapters) != 1 or app_adapters[0]["path"] != app_relative or app_adapters[0]["status"] != "native":
        errors.append("Missing native Airtable mapping adapter")
    return errors


if __name__ == "__main__":
    failures = validate()
    print(json.dumps({"ok": not failures, "errors": failures,
                      "skills": sorted(EXPECTED)}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(failures))

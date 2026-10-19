"""Regression: an installable workflow must expose its required data connector."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("hyundai_validator", ROOT / "scripts/validate_hyundai_skills.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class Distribution(unittest.TestCase):
    def setUp(self):
        fixture_parent = ROOT / "artifacts/hyundai-distribution-tests"
        fixture_parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=fixture_parent)
        if not Path(self.temp.name).resolve().is_relative_to(fixture_parent.resolve()):
            raise RuntimeError("Fixture path escaped its disposable test directory")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plugin = self.root / "plugins/insideout-hyundai-social"
        shutil.copytree(ROOT / "plugins/insideout-hyundai-social", self.plugin)
        for name in (".agents/plugins/marketplace.json", ".agent-smith/index.json"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        self.addCleanup(patch.stopall)
        patch.object(validator, "REPO", self.root).start()
        patch.object(validator, "PLUGIN", self.plugin).start()

    def edit(self, path, change):
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_current_package_has_complete_connection_contract(self):
        self.assertEqual(validator.validate(), [])

    def test_skills_only_manifest_does_not_pass(self):
        self.edit(self.plugin / ".codex-plugin/plugin.json", lambda d: d.pop("apps"))
        self.assertIn("Plugin must declare its Airtable app mapping", validator.validate())

    def test_missing_connector_file_does_not_pass(self):
        (self.plugin / ".app.json").unlink()
        self.assertIn("Missing Airtable app mapping", validator.validate())

    def test_optional_or_wrong_connector_does_not_pass(self):
        original = json.loads((self.plugin / ".app.json").read_text(encoding="utf-8"))
        for replacement in ({"required": False}, {"id": "asdk_app_example_wrong"}):
            with self.subTest(replacement=replacement):
                (self.plugin / ".app.json").write_text(json.dumps(original), encoding="utf-8")
                self.edit(self.plugin / ".app.json", lambda d: d["apps"]["airtable"].update(replacement))
                self.assertIn("App mapping must require the official Airtable connector only", validator.validate())

    def test_deferred_authentication_does_not_pass(self):
        path = self.root / ".agents/plugins/marketplace.json"
        self.edit(path, lambda d: next(p for p in d["plugins"] if p["name"] == self.plugin.name)["policy"].update(authentication="ON_USE"))
        self.assertIn("Catalog must request Airtable authentication on install", validator.validate())


if __name__ == "__main__":
    unittest.main()

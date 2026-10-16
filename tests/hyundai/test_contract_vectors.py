"""Executable oracle for the DOCUMENTED wire contract, not a runtime engine.

These synthetic vectors check cross-session fingerprints, semantic edits and
feedback rejection. Behavioral skill evals and browser QA are separate.
"""
from __future__ import annotations

import copy
import hashlib
import json
import unicodedata
import unittest
from datetime import date
from pathlib import Path

FIXTURE = json.loads(Path(__file__).with_name("contract_vectors.json").read_text(encoding="utf-8"))


def normalize(value):
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    raise ValueError("Contract values must be strings, arrays or objects")


def canonical(value):
    return json.dumps(normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(idea):
    idea = normalize(copy.deepcopy(idea))
    idea["models"].sort()
    idea["publications"].sort(key=lambda p: p["publicationKey"])
    idea["references"].sort(key=lambda r: (r["url"], r["label"], r["role"]))
    for publication in idea["publications"]:
        if publication["date"]:
            date.fromisoformat(publication["date"])
    return "sha256:" + hashlib.sha256(canonical(idea).encode("utf-8")).hexdigest()


class ContractVectors(unittest.TestCase):
    def setUp(self):
        self.idea = copy.deepcopy(FIXTURE["idea"])

    def test_language_neutral_vector(self):
        expected = Path(__file__).with_name("fingerprint.txt").read_text(encoding="utf-8").strip()
        self.assertEqual(fingerprint(self.idea), expected)

    def test_reordering_does_not_change_identity_or_hash(self):
        edited = dict(reversed(list(self.idea.items())))
        edited["models"] = list(reversed(edited["models"]))
        edited["publications"] = list(reversed(edited["publications"]))
        self.assertEqual(fingerprint(edited), fingerprint(self.idea))

    def test_semantic_changes_require_new_confirmation(self):
        changes = [
            lambda i: i.update(description="Outra ideia"),
            lambda i: i.update(execution="Outra execução"),
            lambda i: i.update(additionalCost="Custo confirmado"),
            lambda i: i["references"][0].update(url="https://example.org/outra"),
            lambda i: i["references"][0].update(previewDigest="sha256:diferente"),
            lambda i: i["publications"][0].update(date="2026-09-10"),
            lambda i: i["publications"][1].update(adaptation="Outra adaptação"),
        ]
        for change in changes:
            with self.subTest(change=change):
                edited = copy.deepcopy(self.idea)
                change(edited)
                self.assertEqual(edited["ideaKey"], self.idea["ideaKey"])
                self.assertNotEqual(fingerprint(edited), fingerprint(self.idea))

    def test_unicode_and_line_endings_are_portable(self):
        decomposed = unicodedata.normalize("NFD", canonical(self.idea))
        self.assertEqual(fingerprint(json.loads(decomposed)), fingerprint(self.idea))
        self.assertEqual(canonical({"text": "a\r\nb\rc"}), canonical({"text": "a\nb\nc"}))

    def test_invalid_calendar_date_is_rejected(self):
        self.idea["publications"][0]["date"] = "2026-02-30"
        with self.assertRaises(ValueError):
            fingerprint(self.idea)

    def test_content_is_not_reinterpreted_as_approval(self):
        original = "</script><script>alert(1)</script>\n=HYPERLINK(\"https://example.org\")"
        encoded = canonical({"message": original})
        self.assertEqual(json.loads(encoded)["message"], original)
        self.assertNotIn("approval", json.loads(encoded))


if __name__ == "__main__":
    unittest.main()

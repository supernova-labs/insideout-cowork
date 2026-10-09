#!/usr/bin/env python3
"""Validação estrutural determinística do plugin InsideOut Mar Aberto."""
from __future__ import annotations

import csv
import hashlib
from collections import Counter
from datetime import date
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


SHARED_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = SHARED_ROOT.parent.parent
SKILLS_ROOT = PLUGIN_ROOT / "skills"
REPO_ROOT = PLUGIN_ROOT.parent.parent
MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"

SKILLS = (
    "run-mar-aberto",
    "export-stilingue",
    "collect-comments",
    "analyze-sentiment",
    "generate-report",
)
REQUIRED_SHARED = (
    "about-mar-aberto.md",
    "local-state.md",
    "privacy-retention.md",
    "stilingue-contract.md",
    "collection-contract.md",
    "analysis-rubric.md",
    "report-workbook-contract.md",
    "acceptance-map.md",
    "evals/README.md",
    "schemas/run-manifest.schema.json",
    "schemas/run-manifest-v2.schema.json",
    "schemas/run-manifest-v3.schema.json",
    "schemas/run-manifest-v4.schema.json",
    "schemas/coverage-decision.schema.json",
    "schemas/coverage-record.schema.json",
    "schemas/coverage-diagnostic.schema.json",
    "schemas/analysis-record.schema.json",
    "schemas/evidence-record.schema.json",
    "schemas/source-record.schema.json",
    "fixtures/stilingue-valid.csv",
    "fixtures/stilingue-invalid.csv",
    "fixtures/stilingue-duplicate-synthetic.csv",
    "fixtures/comments-synthetic.jsonl",
    "fixtures/comments-raw-with-duplicate-synthetic.jsonl",
    "fixtures/mentions-synthetic.jsonl",
    "fixtures/coverage-synthetic.jsonl",
    "fixtures/coverage-blocked-synthetic.jsonl",
    "fixtures/coverage-diagnostic-synthetic.json",
    "fixtures/coverage-diagnostic-synthetic.md",
    "fixtures/coverage-edge-cases-synthetic.jsonl",
    "fixtures/coverage-decision-limited-synthetic.json",
    "fixtures/analysis-synthetic.jsonl",
    "fixtures/aggregates-synthetic.json",
    "fixtures/evidence-approved-synthetic.jsonl",
    "fixtures/manifest-complete-synthetic.json",
    "fixtures/manifest-complete-v4-synthetic.json",
    "fixtures/manifest-complete-v3-synthetic.json",
    "fixtures/manifest-path-traversal-invalid-synthetic.json",
    "fixtures/orchestration-cases-synthetic.json",
)
FORBIDDEN_TEXT = ("HB20", "insideout-listening", "${CLAUDE_PLUGIN_ROOT}")
SECRET_PATTERN = re.compile(
    r"(?i)(?:sk-[a-z0-9_-]{16,}|gh[opasu]_[a-z0-9]{20,}|"
    r"(?:app|tbl|fld)[A-Za-z0-9]{14,})"
)
STILINGUE_HEADERS = {
    "publication_id",
    "network",
    "publication_url",
    "published_at",
    "title",
}
ACCEPTANCE_TEST_COUNTS = {0: 6, 1: 6, 2: 5, 3: 8, 4: 9, 5: 10, 6: 8, 7: 5, 8: 5, 9: 8}
RELEASE_GATE_TEST_COUNTS = {0: 1, 1: 4, 2: 3, 3: 2}
ANALYSIS_NETWORKS = {"instagram", "youtube", "x", "facebook", "portals"}
COMMENT_NETWORKS = {"instagram", "youtube"}
SOURCE_KINDS = {"mention", "comment", "reply"}
COVERAGE_STATUSES = {"complete", "partial", "unavailable", "not_required", "unsupported"}
SENTIMENTS = {"positive", "negative", "neutral", "mixed", "ambiguous"}
TARGETS = {"i20", "hyundai", "campaign", "influencer", "purchase-price", "competitor", "other"}


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("'\"")
    return result


def validate_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"JSON inválido em {path.relative_to(PLUGIN_ROOT)}: {exc}")
        return None


def validate_jsonl(path: Path, errors: list[str]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"não foi possível ler {path.relative_to(PLUGIN_ROOT)}: {exc}")
        return records
    for line_number, line in enumerate(lines, 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}:{line_number}: {exc.msg}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{path.name}:{line_number}: registro deve ser objeto")
            continue
        records.append(record)
    return records


def read_csv(path: Path) -> tuple[list[dict[str, str]], set[str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), set(reader.fieldnames or [])


def stilingue_errors(rows: list[dict[str, str]], headers: set[str]) -> list[str]:
    failures: list[str] = []
    missing = sorted(STILINGUE_HEADERS - headers)
    if missing:
        failures.append(f"campos obrigatórios ausentes: {', '.join(missing)}")
    if not rows:
        failures.append("a exportação não contém publicações")
    for index, row in enumerate(rows, 2):
        if STILINGUE_HEADERS.issubset(headers):
            if any(not row.get(field, "").strip() for field in STILINGUE_HEADERS):
                failures.append(f"linha {index}: campo obrigatório vazio")
            try:
                date.fromisoformat(row.get("published_at", ""))
            except ValueError:
                failures.append(f"linha {index}: data da publicação inválida")
            parsed = urlsplit(row.get("publication_url", ""))
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                failures.append(f"linha {index}: URL da publicação inválida")
    return failures


def canonical_publication_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    query = urlencode(
        sorted(
            (key, item)
            for key, item in parse_qsl(parsed.query, keep_blank_values=True)
            if not key.lower().startswith("utm_")
            and key.lower() not in {"fbclid", "gclid"}
        )
    )
    return urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            query,
            "",
        )
    )


def require_fields(
    record: dict[str, object], fields: set[str], label: str, errors: list[str]
) -> None:
    missing = sorted(fields - set(record))
    if missing:
        errors.append(f"{label}: campos obrigatórios ausentes: {', '.join(missing)}")


def is_safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if Path(value).is_absolute() or re.match(r"^[A-Za-z]:", value):
        return False
    return ".." not in re.split(r"[\\\\/]+", value)


def contrast_ratio(foreground: str, background: str) -> float:
    def luminance(rgb: str) -> float:
        channels = [int(rgb[-6:][i:i + 2], 16) / 255 for i in (0, 2, 4)]
        linear = [value / 12.92 if value <= 0.04045 else
                  ((value + 0.055) / 1.055) ** 2.4 for value in channels]
        return sum(value * weight for value, weight in
                   zip(linear, (0.2126, 0.7152, 0.0722)))

    light, dark = sorted((luminance(foreground), luminance(background)),
                         reverse=True)
    return (light + 0.05) / (dark + 0.05)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED_SHARED:
        path = SHARED_ROOT / relative
        if not path.is_file():
            errors.append(f"referência compartilhada ausente: {relative}")

    skill_files: list[Path] = []
    eval_count = 0
    for name in SKILLS:
        skill_dir = SKILLS_ROOT / name
        skill_file = skill_dir / "SKILL.md"
        agent_file = skill_dir / "agents" / "openai.yaml"
        if not skill_file.is_file():
            errors.append(f"{name}: SKILL.md ausente")
            continue
        skill_files.append(skill_file)
        text = skill_file.read_text(encoding="utf-8")
        meta = frontmatter(text)
        if meta.get("name") != name:
            errors.append(f"{name}: frontmatter name divergente")
        if not meta.get("description"):
            errors.append(f"{name}: description ausente")
        line_count = text.count("\n") + 1
        if line_count >= 500:
            errors.append(f"{name}: SKILL.md tem {line_count} linhas (limite <500)")
        resource_paths = re.findall(
            r"`((?:\.\./\.\./references|assets)/[^`]+\.(?:md|json|css))`",
            text,
        )
        for resource in resource_paths:
            resolved_resource = (skill_dir / resource).resolve()
            try:
                resolved_resource.relative_to(PLUGIN_ROOT.resolve())
            except ValueError:
                errors.append(f"{name}: referência escapa do plugin: {resource}")
                continue
            if not resolved_resource.is_file():
                errors.append(f"{name}: referência não resolvida: {resource}")
        if not agent_file.is_file():
            errors.append(f"{name}: agents/openai.yaml ausente")
        else:
            agent_text = agent_file.read_text(encoding="utf-8")
            if f"${name}" not in agent_text:
                errors.append(f"{name}: default_prompt não menciona ${name}")

        evals = sorted((skill_dir / "evals").glob("*.md"))
        eval_count += len(evals)
        if len(evals) < 3:
            errors.append(f"{name}: menos de 3 evals versionados")
        for eval_file in evals:
            eval_text = eval_file.read_text(encoding="utf-8")
            for heading in ("## Prompt", "## Resultado esperado"):
                if heading not in eval_text:
                    errors.append(
                        f"{eval_file.relative_to(PLUGIN_ROOT)}: seção {heading!r} ausente"
                    )

    manifest = validate_json(MANIFEST, errors) if MANIFEST.is_file() else None
    if not MANIFEST.is_file():
        errors.append("manifesto Codex ausente")
    elif isinstance(manifest, dict):
        if manifest.get("name") != "insideout-mar-aberto":
            errors.append("manifesto: name deve ser insideout-mar-aberto")
        version = str(manifest.get("version", ""))
        version_match = re.fullmatch(r"(\d+\.\d+\.\d+)(?:\+codex\.[0-9]+)?", version)
        readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        declared = re.search(r"Versão candidata:\s*(\d+\.\d+\.\d+)", readme_text)
        if not version_match or not declared or version_match.group(1) != declared.group(1):
            errors.append("manifesto: versão não coincide com a versão candidata do README")
        if manifest.get("skills") != "./skills/":
            errors.append("manifesto: skills deve apontar para ./skills/")

    marketplace = validate_json(MARKETPLACE, errors) if MARKETPLACE.is_file() else None
    if isinstance(marketplace, dict):
        entries = {item.get("name"): item for item in marketplace.get("plugins", [])}
        entry = entries.get("insideout-mar-aberto")
        if entry is None:
            errors.append("marketplace: entrada insideout-mar-aberto ausente")
        else:
            source = entry.get("source", {})
            if source.get("path") != "./plugins/insideout-mar-aberto":
                errors.append("marketplace: caminho do Mar Aberto divergente")
            if entry.get("policy", {}).get("authentication") != "ON_USE":
                errors.append("marketplace: autenticação do Mar Aberto deve ser ON_USE")
        if "insideout-social" not in entries:
            errors.append("marketplace: insideout-social foi removido")

    for schema_path in sorted((SHARED_ROOT / "schemas").glob("*.json")):
        validate_json(schema_path, errors)
    current_schema = validate_json(
        SHARED_ROOT / "schemas" / "run-manifest.schema.json", errors)
    previous_schema = validate_json(
        SHARED_ROOT / "schemas" / "run-manifest-v4.schema.json", errors)
    if isinstance(current_schema, dict) and isinstance(previous_schema, dict):
        current = current_schema.get("properties", {})
        previous = previous_schema.get("properties", {})
        if (current.get("contract_version", {}).get("const") != "4.1.0"
            or previous.get("contract_version", {}).get("const") != "4.0.0"
            or current.get("coverage_mode", {}).get("enum")
            != ["complete", "observed_with_gaps"]
            or "blocked_coverage" in current.get("status", {}).get("enum", [])):
            errors.append("schemas 4.1.0 e 4.0.0 não separam as políticas de cobertura")
        paths = current.get("paths", {}).get("properties", {})
        hashes = current.get("hashes", {}).get("properties", {})
        for key, filename in (("coverage_diagnostic", "coverage/diagnostic.json"),
                              ("coverage_summary", "coverage/diagnostic.md")):
            if paths.get(key, {}).get("const") != filename or key not in hashes:
                errors.append(f"manifesto 4.1.0 não registra {filename} e hash")
    diagnostic_schema = validate_json(
        SHARED_ROOT / "schemas" / "coverage-diagnostic.schema.json", errors)
    if isinstance(diagnostic_schema, dict):
        required = set(diagnostic_schema.get("required", []))
        if not {"status", "required_publications", "complete", "partial",
                "unavailable", "observed_comments", "observed_replies",
                "gaps", "counter_note"}.issubset(required):
            errors.append("schema do diagnóstico omite contagens ou diferenças")

    valid_csv = SHARED_ROOT / "fixtures" / "stilingue-valid.csv"
    if valid_csv.is_file():
        rows, headers = read_csv(valid_csv)
        valid_failures = stilingue_errors(rows, headers)
        if valid_failures:
            errors.append(
                "fixture Stilingue válida foi rejeitada: " + "; ".join(valid_failures)
            )
        networks = {row.get("network", "").lower() for row in rows}
        if networks != {"instagram", "youtube", "x", "facebook", "portal", "tiktok"}:
            errors.append("fixture Stilingue não cobre cinco canais analíticos e um não suportado")

        invalid_rows, invalid_headers = read_csv(
            SHARED_ROOT / "fixtures" / "stilingue-invalid.csv"
        )
        invalid_failures = stilingue_errors(invalid_rows, invalid_headers)
        if not any("publication_url" in failure for failure in invalid_failures):
            errors.append("fixture Stilingue inválida não prova a lacuna da URL")

        duplicate_rows, duplicate_headers = read_csv(
            SHARED_ROOT / "fixtures" / "stilingue-duplicate-synthetic.csv"
        )
        duplicate_failures = stilingue_errors(duplicate_rows, duplicate_headers)
        if duplicate_failures:
            errors.append(
                "fixture de URLs repetidas é inválida: " + "; ".join(duplicate_failures)
            )
        canonical_urls = [
            canonical_publication_url(row["publication_url"]) for row in duplicate_rows
        ]
        if len(canonical_urls) != 3 or len(set(canonical_urls)) != 2:
            errors.append("normalização não deduplica três ocorrências em duas publicações")

    mentions = validate_jsonl(
        SHARED_ROOT / "fixtures" / "mentions-synthetic.jsonl", errors
    )
    forbidden_fields = {"username", "author", "profile", "photo", "author_url"}
    mention_ids = [str(record.get("record_id", "")) for record in mentions]
    if len(mention_ids) != len(set(mention_ids)):
        errors.append("fixture de menções contém duplicatas")
    if {str(record.get("network")) for record in mentions} != ANALYSIS_NETWORKS:
        errors.append("fixture de menções não cobre exatamente os cinco canais analíticos")
    for record in mentions:
        leaked = forbidden_fields.intersection(record)
        if leaked:
            errors.append(f"fixture de menções contém identidade: {sorted(leaked)}")
        if record.get("source_kind") != "mention" or record.get("parent_id") is not None:
            errors.append("fixture de menções não preserva source_kind ou parent_id")
        if not re.fullmatch(r"men_[a-f0-9]{16}", str(record.get("record_id", ""))):
            errors.append("fixture de menções usa identificador não anonimizado")

    comments = SHARED_ROOT / "fixtures" / "comments-synthetic.jsonl"
    if comments.is_file():
        records = validate_jsonl(comments, errors)
        if not records or not any(record.get("parent_id") for record in records):
            errors.append("fixture de comentários precisa cobrir resposta aninhada")
        record_ids = [str(record.get("record_id", "")) for record in records]
        if len(record_ids) != len(set(record_ids)):
            errors.append("fixture canônica de comentários contém duplicatas")
        for record in records:
            leaked = forbidden_fields.intersection(record)
            if leaked:
                errors.append(f"fixture de comentários contém identidade: {sorted(leaked)}")
            if not re.fullmatch(r"cmt_[a-f0-9]{16}", str(record.get("record_id", ""))):
                errors.append("fixture de comentários usa identificador não anonimizado")
            if record.get("network") not in COMMENT_NETWORKS:
                errors.append("fixture de comentários contém rede fora da coleta")
            expected_kind = "reply" if record.get("parent_id") else "comment"
            if record.get("source_kind") != expected_kind:
                errors.append("fixture de comentários não preserva source_kind")

        raw_duplicate = validate_jsonl(
            SHARED_ROOT / "fixtures" / "comments-raw-with-duplicate-synthetic.jsonl",
            errors,
        )
        raw_ids = [str(record.get("record_id", "")) for record in raw_duplicate]
        duplicate_ids = {item for item, count in Counter(raw_ids).items() if count > 1}
        if not duplicate_ids or set(record_ids).intersection(duplicate_ids) != duplicate_ids:
            errors.append("fixture bruta não prova deduplicação para a fixture canônica")

        coverage = validate_jsonl(
            SHARED_ROOT / "fixtures" / "coverage-synthetic.jsonl", errors
        )
        coverage_required = {
            "publication_id",
            "network",
            "collection_required",
            "status",
            "observed_comments",
            "observed_replies",
            "exhaustion_evidence",
        }
        for item in coverage:
            label = f"cobertura {item.get('publication_id')}"
            require_fields(item, coverage_required, label, errors)
            if item.get("status") not in COVERAGE_STATUSES:
                errors.append(f"{label}: estado inválido")
            for field in ("observed_comments", "observed_replies"):
                value = item.get(field)
                if type(value) is not int or value < 0:
                    errors.append(f"{label}: {field} deve ser inteiro não negativo")
            if item.get("status") in {"partial", "unavailable", "unsupported"} and not item.get("failure_reason"):
                errors.append(f"{label}: cobertura não completa sem motivo")
            if item.get("collection_required") is True:
                if item.get("network") not in COMMENT_NETWORKS:
                    errors.append(f"{label}: coleta obrigatória fora de Instagram/YouTube")
                if item.get("status") == "complete" and not item.get("exhaustion_evidence"):
                    errors.append(f"{label}: completa sem evidência de esgotamento")
                platform_count = item.get("platform_reported_comments")
                observed_total = int(item.get("observed_comments", 0)) + int(item.get("observed_replies", 0))
                if item.get("status") == "complete" and isinstance(platform_count, int) and platform_count > observed_total:
                    errors.append(f"{label}: completa apesar de contador visível maior")
            elif item.get("status") not in {"not_required", "unsupported"}:
                errors.append(f"{label}: canal sem coleta com estado incompatível")
        coverage_statuses = Counter(str(record.get("status")) for record in coverage)
        if coverage_statuses != Counter({"complete": 2, "not_required": 3, "unsupported": 1}):
            errors.append("fixture de cobertura não diferencia coleta, menção e canal não suportado")
        observed = sum(
            int(record.get("observed_comments", 0))
            + int(record.get("observed_replies", 0))
            for record in coverage
        )
        if observed != len(records):
            errors.append("cobertura sintética não reconcilia com comentários observados")

        partial_coverage = validate_jsonl(
            SHARED_ROOT / "fixtures" / "coverage-blocked-synthetic.jsonl", errors
        )
        blocked = partial_coverage[0] if len(partial_coverage) == 1 else {}
        if len(partial_coverage) != 1:
            errors.append("fixture de cobertura parcial deve conter um caso")
        else:
            if (
                blocked.get("status") != "partial"
                or blocked.get("collection_required") is not True
                or blocked.get("export_reported_comments") != 74
                or blocked.get("platform_reported_comments") != 186
                or blocked.get("observed_comments") != 42
            ):
                errors.append("fixture parcial não prova 74/186/42 e coleta parcial")

        diagnostic = validate_json(
            SHARED_ROOT / "fixtures" / "coverage-diagnostic-synthetic.json", errors
        )
        diagnostic_md = (SHARED_ROOT / "fixtures" /
                         "coverage-diagnostic-synthetic.md").read_text(encoding="utf-8")
        if isinstance(diagnostic, dict):
            gap = (diagnostic.get("gaps") or [{}])[0]
            if (diagnostic.get("status") != "observed_with_gaps"
                or diagnostic.get("required_publications") != 1
                or diagnostic.get("complete") != 0
                or diagnostic.get("partial") != 1
                or diagnostic.get("unavailable") != 0
                or diagnostic.get("observed_comments") != 42
                or diagnostic.get("observed_replies") != 0
                or gap.get("publication_id") != blocked.get("publication_id")
                or [gap.get("export_reported_comments"),
                    gap.get("platform_reported_comments"),
                    gap.get("observed_comments")] != [74, 186, 42]):
                errors.append("diagnóstico estruturado não reconcilia com a coleta parcial")
        for marker in ("1 publicação obrigatória", "0 completas", "1 parcial",
                       "74", "186", "42", "não comprova", "Retomar a coleta",
                       "análise dos itens observados"):
            if marker not in diagnostic_md:
                errors.append(f"diagnóstico legível sem {marker}")
        if re.search(r"pub-ig-|https?://|shortcode|@", diagnostic_md, re.I):
            errors.append("diagnóstico legível contém identificador ou URL")

        edge_coverage = validate_jsonl(
            SHARED_ROOT / "fixtures" / "coverage-edge-cases-synthetic.jsonl", errors
        )
        zero_case = next(
            (item for item in edge_coverage if item.get("publication_id") == "pub-zero-001"),
            None,
        )
        unavailable_case = next(
            (
                item
                for item in edge_coverage
                if item.get("publication_id") == "pub-private-001"
            ),
            None,
        )
        if not zero_case or zero_case.get("status") != "complete" or any(
            int(zero_case.get(field, 0)) != 0
            for field in ("observed_comments", "observed_replies")
        ):
            errors.append("caso sem comentários não fecha como cobertura completa com zero")
        stilingue_divergence_case = next(
            (
                item
                for item in edge_coverage
                if item.get("publication_id") == "pub-stilingue-divergence-001"
            ),
            None,
        )
        if (
            not stilingue_divergence_case
            or stilingue_divergence_case.get("status") != "complete"
            or stilingue_divergence_case.get("export_reported_comments") != 186
            or stilingue_divergence_case.get("platform_reported_comments") is not None
            or stilingue_divergence_case.get("observed_comments") != 0
            or not stilingue_divergence_case.get("exhaustion_evidence")
        ):
            errors.append(
                "divergência da Stilingue sem contador visível não fecha como cobertura observável"
            )
        if (
            not unavailable_case
            or unavailable_case.get("status") != "unavailable"
            or not unavailable_case.get("failure_reason")
        ):
            errors.append("caso indisponível não preserva estado e motivo")

        analyses = validate_jsonl(
            SHARED_ROOT / "fixtures" / "analysis-synthetic.jsonl", errors
        )
        source_ids = set(record_ids) | set(mention_ids)
        if {str(record.get("record_id")) for record in analyses} != source_ids:
            errors.append("análises sintéticas não reconciliam menções e comentários")
        analysis_forbidden = forbidden_fields | {"text", "verbatim_text", "comment"}
        sentiment_counts: Counter[str] = Counter()
        source_counts: dict[str, Counter[str]] = {
            kind: Counter() for kind in SOURCE_KINDS
        }
        amplification: dict[str, dict[str, Counter[str]]] = {}
        for record in analyses:
            label = f"análise {record.get('record_id')}"
            require_fields(
                record,
                {
                    "record_id",
                    "publication_id",
                    "network",
                    "source_kind",
                    "published_at",
                    "relevant",
                    "targets",
                    "target_sentiments",
                    "sentiment",
                    "themes",
                    "confidence",
                    "engagement",
                },
                label,
                errors,
            )
            leaked = analysis_forbidden.intersection(record)
            if leaked:
                errors.append(f"análise sintética contém texto ou identidade: {sorted(leaked)}")
            if record.get("network") not in ANALYSIS_NETWORKS:
                errors.append(f"{label}: rede não suportada entrou na análise")
            if record.get("source_kind") not in SOURCE_KINDS:
                errors.append(f"{label}: tipo de fonte inválido")
            if type(record.get("relevant")) is not bool:
                errors.append(f"{label}: relevância deve ser booleana")
            if record.get("sentiment") not in SENTIMENTS:
                errors.append(f"{label}: sentimento inválido")
            confidence = record.get("confidence")
            if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
                errors.append(f"{label}: confiança fora do intervalo 0–1")
            if record.get("relevant") is False and not record.get("relevance_reason"):
                errors.append(f"{label}: exclusão sem motivo")
            targets = set(record.get("targets", []))
            if not targets.issubset(TARGETS) or len(targets) != len(record.get("targets", [])):
                errors.append(f"{label}: alvos inválidos ou repetidos")
            target_sentiments = record.get("target_sentiments", [])
            mapped_targets = {
                str(item.get("target"))
                for item in target_sentiments
                if isinstance(item, dict)
            }
            if not targets or targets != mapped_targets:
                errors.append(
                    f"{record.get('record_id')}: sentimentos por alvo não reconciliam com alvos"
                )
            for item in target_sentiments:
                if not isinstance(item, dict):
                    errors.append(f"{label}: sentimento por alvo não é objeto")
                    continue
                require_fields(item, {"target", "sentiment", "confidence"}, label, errors)
                item_confidence = item.get("confidence")
                if item.get("target") not in TARGETS or item.get("sentiment") not in SENTIMENTS:
                    errors.append(f"{label}: sentimento por alvo inválido")
                if not isinstance(item_confidence, (int, float)) or isinstance(item_confidence, bool) or not 0 <= item_confidence <= 1:
                    errors.append(f"{label}: confiança por alvo fora do intervalo 0–1")
            themes = record.get("themes", [])
            if not isinstance(themes, list) or not themes or len(themes) != len(set(themes)):
                errors.append(f"{label}: temas devem ser lista não vazia e sem duplicatas")
            if record.get("relevant") is True:
                sentiment_counts[str(record.get("sentiment"))] += 1
                source_kind = str(record.get("source_kind"))
                source_counts[source_kind]["relevant"] += 1
                source_counts[source_kind][str(record.get("sentiment"))] += 1
                network = str(record.get("network"))
                engagement = record.get("engagement", {})
                if isinstance(engagement, dict):
                    signals = amplification.setdefault(network, {}).setdefault(source_kind, Counter())
                    signals["likes"] += int(engagement.get("likes") or 0)
                    signals["replies"] += int(engagement.get("replies") or 0)
            record_kind = str(record.get("source_kind"))
            if record_kind in source_counts:
                source_counts[record_kind]["observed"] += 1
            if record.get("relevant") is False:
                if record_kind in source_counts:
                    source_counts[record_kind]["excluded"] += 1

        aggregates = validate_json(
            SHARED_ROOT / "fixtures" / "aggregates-synthetic.json", errors
        )
        if isinstance(aggregates, dict):
            if aggregates.get("observed_records") != len(analyses):
                errors.append("agregado observado diverge das análises")
            relevant_count = sum(record.get("relevant") is True for record in analyses)
            if aggregates.get("relevant_records") != relevant_count:
                errors.append("agregado de relevantes diverge das análises")
            if aggregates.get("excluded_records") != len(analyses) - relevant_count:
                errors.append("agregado de excluídos diverge das análises")
            if Counter(aggregates.get("sentiment_distribution", {})) != sentiment_counts:
                errors.append("distribuição de sentimento diverge das análises")
            for kind, counts in source_counts.items():
                expected = aggregates.get("records_by_source_kind", {}).get(kind, {})
                if expected.get("observed") != counts["observed"]:
                    errors.append(f"observados divergem para {kind}")
                if expected.get("relevant") != counts["relevant"]:
                    errors.append(f"relevantes divergem para {kind}")
                if expected.get("excluded") != counts["excluded"]:
                    errors.append(f"excluídos divergem para {kind}")
                expected_sentiments = Counter(expected.get("sentiment_distribution", {}))
                actual_sentiments = Counter({sentiment: counts[sentiment] for sentiment in SENTIMENTS})
                if expected_sentiments != actual_sentiments:
                    errors.append(f"sentimento por fonte diverge para {kind}")
            expected_amplification = aggregates.get("amplification_by_platform_and_source", {})
            for network, by_kind in amplification.items():
                for kind, signals in by_kind.items():
                    expected = expected_amplification.get(network, {}).get(kind, {})
                    if expected.get("likes") != signals["likes"] or expected.get("replies") != signals["replies"]:
                        errors.append(f"amplificação diverge em {network}/{kind}")
                    if expected.get("signal_total") != signals["likes"] + signals["replies"]:
                        errors.append(f"total de amplificação diverge em {network}/{kind}")
            daily = aggregates.get("daily_sentiment", [])
            if not isinstance(daily, list) or not daily:
                errors.append("agregados não incluem séries diárias")
            else:
                daily_total = 0
                for item in daily:
                    counted = sum(int(item.get(sentiment, 0)) for sentiment in SENTIMENTS)
                    if counted != item.get("total"):
                        errors.append("série diária não reconcilia sentimento e total")
                    daily_total += counted
                if daily_total != sum(sentiment_counts.values()):
                    errors.append("séries diárias não reconciliam registros relevantes")

        evidences = validate_jsonl(
            SHARED_ROOT / "fixtures" / "evidence-approved-synthetic.jsonl", errors
        )
        source_text = {
            str(record["record_id"]): record.get("text")
            for record in [*mentions, *records]
        }
        evidence_roles = {str(record.get("selection_role")) for record in evidences}
        if evidence_roles != {"recurring", "striking", "counterpoint"}:
            errors.append("pool de evidências não cobre os três papéis de seleção")
        for evidence in evidences:
            label = f"evidência {evidence.get('record_id')}"
            require_fields(
                evidence,
                {
                    "record_id",
                    "publication_id",
                    "network",
                    "source_kind",
                    "verbatim_text",
                    "sentiment",
                    "themes",
                    "selection_role",
                    "approved",
                },
                label,
                errors,
            )
            if evidence.get("approved") is not True:
                errors.append("pool aprovado contém evidência sem aprovação")
            if evidence.get("network") not in ANALYSIS_NETWORKS:
                errors.append(f"{label}: rede inválida")
            if evidence.get("source_kind") not in SOURCE_KINDS:
                errors.append(f"{label}: tipo de fonte inválido")
            if evidence.get("sentiment") not in SENTIMENTS:
                errors.append(f"{label}: sentimento inválido")
            if evidence.get("selection_role") not in {"recurring", "striking", "counterpoint"}:
                errors.append(f"{label}: papel de seleção inválido")
            if source_text.get(str(evidence.get("record_id"))) != evidence.get("verbatim_text"):
                errors.append("texto de evidência não coincide com o corpus sintético")
            if forbidden_fields.intersection(evidence):
                errors.append("evidência sintética contém identidade")

        manifest = validate_json(
            SHARED_ROOT / "fixtures" / "manifest-complete-synthetic.json", errors
        )
        if isinstance(manifest, dict):
            require_fields(
                manifest,
                {"contract_version", "run_id", "project", "filter", "period", "status", "stage", "paths"},
                "manifesto",
                errors,
            )
            if manifest.get("contract_version") != "4.1.0":
                errors.append("manifesto: versão de contrato divergente")
            if set(manifest.get("hashes", {})) != {
                "report_template", "analytics_template", "report", "analytics",
                "coverage_diagnostic", "coverage_summary"
            } or manifest.get("template_version") != "0.5.0":
                errors.append("manifesto completo não registra templates e diagnósticos")
            if manifest.get("coverage_mode") != "complete":
                errors.append("manifesto completo não registra modo de cobertura")
            if not {"report", "workbook", "report_template", "analytics_template",
                    "coverage_diagnostic", "coverage_summary"}.issubset(
                manifest.get("paths", {})
            ):
                errors.append("manifesto completo não registra entregáveis, templates e diagnósticos")
            elif any(manifest["paths"].get(key) != expected for key, expected in {
                "report": "deliverables/report.html",
                "workbook": "deliverables/analytics.xlsx",
                "report_template": "templates/report-template.html",
                "analytics_template": "templates/analytics-template.xlsx",
                "coverage_diagnostic": "coverage/diagnostic.json",
                "coverage_summary": "coverage/diagnostic.md",
            }.items()):
                errors.append("manifesto completo não usa os caminhos do contrato 4.1.0")
            if manifest.get("status") != "completed" or manifest.get("stage") != "complete":
                errors.append("manifesto sintético final não está concluído")
            period = manifest.get("period", {})
            if not isinstance(period, dict):
                errors.append("manifesto: período inválido")
            else:
                try:
                    start = date.fromisoformat(str(period.get("start", "")))
                    end = date.fromisoformat(str(period.get("end", "")))
                    if start > end:
                        errors.append("manifesto: período invertido")
                except ValueError:
                    errors.append("manifesto: data de período inválida")
                if period.get("timezone") != "America/Sao_Paulo":
                    errors.append("manifesto: fuso divergente")
            paths = manifest.get("paths", {})
            for name, value in paths.items():
                if not is_safe_relative_path(value):
                    errors.append(f"manifesto: caminho {name} não é relativo e confinado")
            counts = manifest.get("counts", {})
            expected_counts = {
                "publications": len(coverage),
                "mentions": len(mentions),
                "comments": sum(record.get("source_kind") == "comment" for record in records),
                "replies": sum(record.get("source_kind") == "reply" for record in records),
                "observed_records": len(analyses),
                "relevant_records": sum(record.get("relevant") is True for record in analyses),
                "evidence": len(evidences),
            }
            if counts != expected_counts:
                errors.append("manifesto completo não reconcilia suas contagens")

        legacy_v4 = validate_json(
            SHARED_ROOT / "fixtures" / "manifest-complete-v4-synthetic.json", errors
        )
        if isinstance(legacy_v4, dict):
            if (legacy_v4.get("contract_version") != "4.0.0"
                or legacy_v4.get("paths", {}).get("report") != "deliverables/report.html"
                or legacy_v4.get("coverage_mode") is not None
                or legacy_v4.get("template_version") != "0.4.0"):
                errors.append("fixture legada 4.0.0 foi migrada para o contrato novo")

        legacy_v3 = validate_json(
            SHARED_ROOT / "fixtures" / "manifest-complete-v3-synthetic.json", errors
        )
        if isinstance(legacy_v3, dict):
            if (legacy_v3.get("contract_version") != "3.0.0"
                or legacy_v3.get("paths", {}).get("report") != "deliverables/report.pptx"
                or legacy_v3.get("paths", {}).get("report_template")
                != "templates/report-template.pptx"
                or legacy_v3.get("template_version") != "0.3.0"):
                errors.append("fixture legada 3.0.0 foi migrada para o contrato novo")

        invalid_paths = validate_json(
            SHARED_ROOT / "fixtures" / "manifest-path-traversal-invalid-synthetic.json",
            errors,
        )
        if isinstance(invalid_paths, dict):
            candidates = invalid_paths.get("paths", {})
            if not isinstance(candidates, dict) or not candidates or any(
                is_safe_relative_path(value) for value in candidates.values()
            ):
                errors.append("fixture de path traversal não é rejeitada integralmente")

        coverage_decision = validate_json(
            SHARED_ROOT / "fixtures" / "coverage-decision-limited-synthetic.json",
            errors,
        )
        if (
            not isinstance(coverage_decision, dict)
            or coverage_decision.get("decision") != "limited_approved"
            or not coverage_decision.get("approved_at")
            or not coverage_decision.get("gaps")
        ):
            errors.append("fixture de decisão limitada não registra aprovação e lacunas")

        orchestration = validate_json(
            SHARED_ROOT / "fixtures" / "orchestration-cases-synthetic.json", errors
        )
        if isinstance(orchestration, dict):
            ordered = orchestration.get("ordered_stages", [])
            expected_order = [
                "export",
                "collection",
                "analysis",
                "editorial_gate_1",
                "report",
                "complete",
            ]
            if ordered != expected_order:
                errors.append("sequência sintética diverge da orquestração canônica")
            for case in orchestration.get("resume_cases", []):
                last_stage = case.get("last_valid_stage")
                next_stage = case.get("next_stage")
                if case.get("repeated_stages"):
                    errors.append(f"retomada em {last_stage} repete etapa concluída")
                if last_stage == "complete":
                    if next_stage is not None:
                        errors.append("execução concluída possui próxima etapa")
                elif last_stage in ordered:
                    expected_next = ordered[ordered.index(last_stage) + 1]
                    if next_stage != expected_next:
                        errors.append(f"retomada após {last_stage} não avança para {expected_next}")
            pause_reasons = {
                str(case.get("reason")) for case in orchestration.get("pause_cases", [])
            }
            if pause_reasons != {
                "expired_instagram_session",
                "missing_collection_checkpoint",
                "gate_1_rejected",
                "missing_workbook",
                "invalid_input",
            }:
                errors.append("casos de pausa não cobrem sessão, checkpoint, Gate 1 e planilha ausente")
            gaps_case = orchestration.get("coverage_gaps_case", {})
            if gaps_case != {
                "prior_status": "in_progress",
                "status": "in_progress",
                "stage": "analysis",
                "coverage_mode": "observed_with_gaps",
                "requires": "all_required_checkpointed",
            }:
                errors.append("caso de lacuna não promove análise após fechar a fila")
            if orchestration.get("material_claim_case") != {
                "stage": "editorial_gate_1",
                "requires": "resume_or_revise_claim",
                "forbid": ["report", "complete"],
            }:
                errors.append("Gate 1 não trata conclusão materialmente afetada")

    assets = SKILLS_ROOT / "generate-report" / "assets"
    template_manifest = validate_json(assets / "template-manifest.json", errors)
    if isinstance(template_manifest, dict):
        if template_manifest.get("template_version") != "0.5.0":
            errors.append("generate-report: versão dos templates divergente")
        for key, filename in (("report_template", "report-template.html"),
                              ("analytics_template", "analytics-template.xlsx")):
            entry = template_manifest.get(key, {})
            path = assets / filename
            template_bytes = path.read_bytes() if path.is_file() else b""
            if filename.endswith(".html"):
                # Git normaliza LF; o checkout do Windows pode materializar CRLF.
                template_bytes = template_bytes.replace(b"\r\n", b"\n")
            if entry.get("path") != filename or (
                path.is_file() and
                entry.get("sha256") != hashlib.sha256(template_bytes).hexdigest()
            ):
                errors.append(f"generate-report: hash do template divergente: {filename}")
    html_template = assets / "report-template.html"
    if html_template.is_file():
        html_text = html_template.read_text(encoding="utf-8")
        html_content = re.sub(r'(?is)<template id="inter-license".*?</template>',
                              '', html_text)
        for marker in ("<!doctype html>", 'lang="pt-BR"', "{{COVER_IMAGE_DATA_URI}}",
                       "{{SCOPE_LABEL}}",
                       "{{SENTIMENT_DISTRIBUTIONS}}", "{{CHANNEL_THEME_MAP}}",
                       "{{SERIES_PANELS}}", "{{COVERAGE_GAPS}}",
                       "{{COUNTER_COMPARISON}}", "{{FOOTER}}",
                       "class=\"sheet", ".theme-map{", "@media print",
                       'id="component-sentiment-row"', 'id="component-theme-map"',
                       'id="component-bar-chart"', 'id="component-evidence"'):
            if marker not in html_text:
                errors.append(f"generate-report: HTML modelo sem {marker}")
        if re.search(r"(?is)<script\b|https?://|<iframe\b|<form\b", html_content):
            errors.append("generate-report: HTML modelo contém script ou recurso externo")
        if "{{COVERAGE_BADGE}}" in html_content:
            errors.append("generate-report: selo geral de cobertura ainda se repete")
        if re.search(r"(?i)@[a-z0-9.-]+\.[a-z]{2,}|2026[-/]0[89][-/]\d{1,2}|"
                     r"22\.738\.981|9\.915\.988|303\.388|2\.139", html_content):
            errors.append("generate-report: HTML modelo contém dado histórico ou pessoal")
        if "{{" in re.sub(r"\{\{[A-Z_]+\}\}", "", html_content):
            errors.append("generate-report: placeholders HTML incompletos")
        if 'id="inter-license"' not in html_text:
            errors.append("generate-report: licença da fonte incorporada ausente")
        page_number_color = re.search(
            r"\.page-number\{[^}]*color:#([0-9a-fA-F]{6})", html_content)
        if not page_number_color or contrast_ratio(
            page_number_color.group(1), "ffffff") < 4.5:
            errors.append("generate-report: número de página com baixo contraste")
    else:
        errors.append("generate-report: template ausente: report-template.html")
    for filename, required_parts in (
        ("analytics-template.xlsx", ("xl/workbook.xml", "xl/worksheets/sheet8.xml")),
    ):
        path = assets / filename
        if not path.is_file() or not zipfile.is_zipfile(path):
            errors.append(f"generate-report: template ausente ou ilegível: {filename}")
            continue
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if not set(required_parts).issubset(names):
                errors.append(f"generate-report: template incompleto: {filename}")
            if any("externalLinks" in name or "comments" in name.lower() or
                   "vbaProject" in name for name in names):
                errors.append(f"generate-report: template contém vínculo ou comentário: {filename}")
            sheets = [name for name in names if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", name)]
            if len(sheets) != 8 or len([name for name in names if name.startswith("xl/tables/table")]) != 6:
                errors.append("generate-report: XLSX não contém oito abas e filtros")
            if "xl/styles.xml" in names:
                styles_root = ElementTree.fromstring(archive.read("xl/styles.xml"))
                local_name = lambda node: node.tag.rsplit("}", 1)[-1]
                style_group = lambda label: next(
                    (node for node in styles_root if local_name(node) == label), None)
                fonts_group = style_group("fonts")
                fills_group = style_group("fills")
                cell_styles_group = style_group("cellXfs")
                fonts = list(fonts_group) if fonts_group is not None else []
                fills = list(fills_group) if fills_group is not None else []
                cell_styles = list(cell_styles_group) if cell_styles_group is not None else []
                low_contrast: list[str] = []
                for sheet_name in sheets:
                    sheet_root = ElementTree.fromstring(archive.read(sheet_name))
                    for cell in sheet_root.iter():
                        if local_name(cell) != "c" or not any(
                            local_name(node) == "t" and (node.text or "").strip()
                            for node in cell.iter()
                        ):
                            continue
                        style_id = int(cell.attrib.get("s", "0"))
                        if style_id >= len(cell_styles):
                            continue
                        style = cell_styles[style_id]
                        font_id = int(style.attrib.get("fontId", "0"))
                        fill_id = int(style.attrib.get("fillId", "0"))
                        if font_id >= len(fonts) or fill_id >= len(fills):
                            continue
                        font_color = next((node.attrib.get("rgb") for node in fonts[font_id]
                                           if local_name(node) == "color"), None)
                        pattern = next((node for node in fills[fill_id]
                                        if local_name(node) == "patternFill"), None)
                        fill_color = next((node.attrib.get("rgb") for node in pattern
                                           if local_name(node) == "fgColor"), None) if (
                                               pattern is not None and
                                               pattern.attrib.get("patternType") == "solid") else None
                        if font_color and fill_color and contrast_ratio(
                            font_color, fill_color) < 4.5:
                            low_contrast.append(f"{sheet_name}:{cell.attrib.get('r', '?')}")
                if low_contrast:
                    errors.append("generate-report: XLSX contém texto com baixo contraste: " +
                                  ", ".join(low_contrast[:8]) +
                                  (f" (+{len(low_contrast) - 8})" if len(low_contrast) > 8 else ""))
            for sheet_name in sheets:
                sheet_xml = archive.read(sheet_name).decode("utf-8")
                if not re.search(r"<(?:[a-zA-Z0-9]+:)?pane\s", sheet_xml):
                    errors.append(f"generate-report: cabeçalho não congelado: {sheet_name}")
                if re.search(r"<(?:[a-zA-Z0-9]+:)?f(?:\s|>)", sheet_xml):
                    errors.append(f"generate-report: fórmula no template: {sheet_name}")
            for sheet_name in ("xl/worksheets/sheet5.xml", "xl/worksheets/sheet6.xml"):
                if sheet_name in names:
                    legend = archive.read(sheet_name).decode("utf-8")
                    if not all(label in legend for label in
                               ("Positivo", "Neutro", "Negativo", "Misto", "Indefinido")):
                        errors.append(f"generate-report: legenda incompleta: {sheet_name}")
            if "xl/worksheets/sheet3.xml" in names:
                publications = archive.read("xl/worksheets/sheet3.xml").decode("utf-8")
                for label in ("Link da publicação", "Data", "ID da publicação",
                              "Comentários positivos", "Comentários neutros",
                              "Comentários negativos", "Comentários mistos",
                              "Comentários indefinidos", "Total de comentários",
                              "Total de respostas"):
                    if label not in publications:
                        errors.append(f"generate-report: base por publicação sem {label}")
            if "xl/worksheets/sheet1.xml" in names:
                summary = archive.read("xl/worksheets/sheet1.xml").decode("utf-8")
                if "SENTIMENTO POR FONTE" not in summary:
                    errors.append("generate-report: resumo sem sentimento por fonte")
            if "xl/worksheets/sheet6.xml" in names:
                daily = archive.read("xl/worksheets/sheet6.xml").decode("utf-8")
                for label in ("MENÇÕES", "COMENTÁRIOS", "RESPOSTAS"):
                    if label not in daily:
                        errors.append(f"generate-report: painel diário sem {label}")
            chart_paths = sorted(name for name in names if re.fullmatch(
                r"xl/drawings/charts/chart\d+\.xml", name))
            if len(chart_paths) != 3:
                errors.append("generate-report: XLSX sem três gráficos modelo")
            else:
                expected_colors = {"38761D", "F1C232", "CC0000", "8E7CC3", "999999"}
                for chart_path in chart_paths:
                    try:
                        chart_root = ElementTree.fromstring(archive.read(chart_path))
                    except ElementTree.ParseError:
                        errors.append(f"generate-report: gráfico inválido: {chart_path}")
                        continue
                    bar_chart = next((node for node in chart_root.iter()
                                      if node.tag.rsplit("}", 1)[-1] == "barChart"), None)
                    if bar_chart is None:
                        errors.append(f"generate-report: gráfico não é de colunas: {chart_path}")
                        continue
                    properties = {node.tag.rsplit("}", 1)[-1]: node.attrib.get("val")
                                  for node in bar_chart if node.tag.rsplit("}", 1)[-1]
                                  in {"barDir", "grouping", "overlap"}}
                    series = [node for node in bar_chart
                              if node.tag.rsplit("}", 1)[-1] == "ser"]
                    series_titles = [next((value.text for value in item.iter()
                                           if value.tag.rsplit("}", 1)[-1] == "v"), None)
                                     for item in series]
                    colors = {node.attrib.get("val") for node in bar_chart.iter()
                              if node.tag.rsplit("}", 1)[-1] == "srgbClr"}
                    if (properties != {"barDir": "col", "grouping": "percentStacked",
                                       "overlap": "100"} or len(series) != 5 or
                            colors != expected_colors or series_titles !=
                            ["Positivo", "Neutro", "Negativo", "Misto", "Indefinido"]):
                        errors.append(f"generate-report: gráfico fora do modelo: {chart_path}")
            workbook_xml = archive.read("xl/workbook.xml").decode("utf-8")
            for label in ("Resumo", "Cobertura", "Publicações", "Análises",
                          "Agregações", "Séries diárias", "Evidências", "Metodologia"):
                if label not in workbook_xml:
                    errors.append(f"generate-report: aba ausente no template: {label}")
            for name in names:
                if not name.endswith(".xml") or name.startswith("_rels/"):
                    continue
                try:
                    root = ElementTree.fromstring(archive.read(name))
                except ElementTree.ParseError:
                    errors.append(f"generate-report: XML inválido em {filename}: {name}")
                    continue
                text = " ".join(node.text or "" for node in root.iter()
                                if node.tag.rsplit("}", 1)[-1] in {"t", "v"})
                if re.search(r"(?i)@[a-z0-9.-]+\.[a-z]{2,}|2026[-/]0[89][-/]\d{1,2}|https?://", text):
                    errors.append(f"generate-report: conteúdo histórico ou pessoal em {filename}: {name}")

    # Fixture histórica: execuções antigas preservam seus arquivos locais.
    feedback_fixture = SHARED_ROOT / "fixtures" / "feedback-sanitized-synthetic.md"
    if feedback_fixture.is_file():
        feedback_fixture_text = feedback_fixture.read_text(encoding="utf-8")
        if not re.search(r"(?m)^fingerprint: [a-f0-9]{64}$", feedback_fixture_text):
            errors.append("fixture de feedback não possui fingerprint SHA-256")
        for heading in (
            "## Etapa e caso de uso",
            "## Comportamento esperado",
            "## Comportamento observado",
            "## Impacto",
            "## Cobertura e retomada",
            "## Sugestão",
            "## Recorrências",
        ):
            if heading not in feedback_fixture_text:
                errors.append(f"fixture de feedback sem seção {heading}")
        if "status: local" not in feedback_fixture_text:
            errors.append("fixture de feedback não está marcada como local")

    plan_path = REPO_ROOT / "DEVELOPMENT_PLAN_MAR_ABERTO.md"
    acceptance_test_count = 0
    if not plan_path.is_file():
        errors.append("plano de desenvolvimento do Mar Aberto ausente")
    else:
        plan_text = plan_path.read_text(encoding="utf-8")
        test_ids = re.findall(r"(?m)^\|\s+(M\d-T\d+)\s+\|", plan_text)
        expected_test_ids = {
            f"M{milestone}-T{number}"
            for milestone, count in ACCEPTANCE_TEST_COUNTS.items()
            for number in range(1, count + 1)
        }
        acceptance_test_count = len(test_ids)
        if len(test_ids) != len(set(test_ids)):
            errors.append("plano contém IDs de teste duplicados")
        if set(test_ids) != expected_test_ids:
            missing = sorted(expected_test_ids - set(test_ids))
            extra = sorted(set(test_ids) - expected_test_ids)
            errors.append(f"matriz de 70 testes divergente; ausentes={missing}; extras={extra}")

    protocol_path = REPO_ROOT / "docs" / "mar-aberto-pilot-test-protocol.md"
    if not protocol_path.is_file():
        errors.append("protocolo operacional M9 ausente")
    else:
        protocol_text = protocol_path.read_text(encoding="utf-8")
        protocol_ids = re.findall(r"(?m)^###\s+(M9-T\d+)\s+—", protocol_text)
        expected_protocol_ids = {f"M9-T{number}" for number in range(1, 9)}
        if len(protocol_ids) != len(set(protocol_ids)):
            errors.append("protocolo M9 contém IDs de teste duplicados")
        if set(protocol_ids) != expected_protocol_ids:
            missing = sorted(expected_protocol_ids - set(protocol_ids))
            extra = sorted(set(protocol_ids) - expected_protocol_ids)
            errors.append(f"protocolo M9 divergente; ausentes={missing}; extras={extra}")
        for status in ("passou", "falhou", "não executado"):
            if f"`{status}`" not in protocol_text:
                errors.append(f"protocolo M9 não define o estado {status}")
        for decision in ("liberar", "iterar", "interromper"):
            if f"`{decision}`" not in protocol_text:
                errors.append(f"protocolo M9 não define a decisão {decision}")
        if "<ref-publicada>" not in protocol_text:
            errors.append("protocolo M9 não exige uma referência publicada explícita")
        for token in ("0.2.2", "blocked_coverage", "Séries diárias", "Markdown local"):
            if token not in protocol_text:
                errors.append(f"protocolo M9 não cobre {token}")

    release_gates_path = REPO_ROOT / "RELEASE_GATES_MAR_ABERTO_0.2.2.md"
    release_gate_test_count = 0
    if not release_gates_path.is_file():
        errors.append("gates de release 0.2.2 ausentes")
    else:
        release_text = release_gates_path.read_text(encoding="utf-8")
        gate_ids = re.findall(r"(?m)^\|\s+(R022-G\d-T\d+)\s+\|", release_text)
        expected_gate_ids = {
            f"R022-G{gate}-T{number}"
            for gate, count in RELEASE_GATE_TEST_COUNTS.items()
            for number in range(1, count + 1)
        }
        release_gate_test_count = len(gate_ids)
        if len(gate_ids) != len(set(gate_ids)):
            errors.append("gates 0.2.2 contêm IDs duplicados")
        if set(gate_ids) != expected_gate_ids:
            missing = sorted(expected_gate_ids - set(gate_ids))
            extra = sorted(set(gate_ids) - expected_gate_ids)
            errors.append(f"matriz de gates 0.2.2 divergente; ausentes={missing}; extras={extra}")

    text_suffixes = {".md", ".json", ".jsonl", ".csv", ".yaml", ".yml", ".css"}
    inspected = [
        path
        for path in PLUGIN_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in text_suffixes
    ]
    for path in inspected:
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_TEXT:
            if token.lower() in text.lower():
                errors.append(f"{path.relative_to(PLUGIN_ROOT)}: termo proibido {token}")
        if SECRET_PATTERN.search(text):
            errors.append(f"{path.relative_to(PLUGIN_ROOT)}: possível segredo ou ID interno")

    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "skills": list(SKILLS),
        "evals": eval_count,
        "acceptance_tests": acceptance_test_count,
        "release_gate_tests": release_gate_test_count,
        "schemas": len(list((SHARED_ROOT / "schemas").glob("*.json"))),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

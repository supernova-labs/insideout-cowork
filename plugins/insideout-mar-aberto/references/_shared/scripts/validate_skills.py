#!/usr/bin/env python3
"""Validação estrutural determinística do plugin InsideOut Mar Aberto."""
from __future__ import annotations

import csv
from collections import Counter
from datetime import date
import json
import re
from pathlib import Path
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
    "skill-feedback",
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
    "schemas/coverage-record.schema.json",
    "schemas/analysis-record.schema.json",
    "schemas/evidence-record.schema.json",
    "fixtures/stilingue-valid.csv",
    "fixtures/stilingue-invalid.csv",
    "fixtures/stilingue-duplicate-synthetic.csv",
    "fixtures/comments-synthetic.jsonl",
    "fixtures/comments-raw-with-duplicate-synthetic.jsonl",
    "fixtures/coverage-synthetic.jsonl",
    "fixtures/coverage-edge-cases-synthetic.jsonl",
    "fixtures/analysis-synthetic.jsonl",
    "fixtures/aggregates-synthetic.json",
    "fixtures/evidence-approved-synthetic.jsonl",
    "fixtures/manifest-complete-synthetic.json",
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
SUPPORTED_NETWORKS = {"instagram", "youtube"}
COVERAGE_STATUSES = {"complete", "partial", "unavailable", "unsupported"}
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
        if manifest.get("version") != "0.1.0":
            errors.append("manifesto: versão piloto deve ser 0.1.0")
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

    valid_csv = SHARED_ROOT / "fixtures" / "stilingue-valid.csv"
    if valid_csv.is_file():
        rows, headers = read_csv(valid_csv)
        valid_failures = stilingue_errors(rows, headers)
        if valid_failures:
            errors.append(
                "fixture Stilingue válida foi rejeitada: " + "; ".join(valid_failures)
            )
        networks = {row.get("network", "").lower() for row in rows}
        if not {"instagram", "youtube", "tiktok"}.issubset(networks):
            errors.append("fixture Stilingue não cobre suportados e não suportado")

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

    comments = SHARED_ROOT / "fixtures" / "comments-synthetic.jsonl"
    if comments.is_file():
        records = validate_jsonl(comments, errors)
        if not records or not any(record.get("parent_id") for record in records):
            errors.append("fixture de comentários precisa cobrir resposta aninhada")
        forbidden_fields = {"username", "author", "profile", "photo", "author_url"}
        record_ids = [str(record.get("record_id", "")) for record in records]
        if len(record_ids) != len(set(record_ids)):
            errors.append("fixture canônica de comentários contém duplicatas")
        for record in records:
            leaked = forbidden_fields.intersection(record)
            if leaked:
                errors.append(f"fixture de comentários contém identidade: {sorted(leaked)}")
            if not re.fullmatch(r"cmt_[a-f0-9]{16}", str(record.get("record_id", ""))):
                errors.append("fixture de comentários usa identificador não anonimizado")

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
            "status",
            "observed_comments",
            "observed_replies",
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
            if item.get("status") != "complete" and not item.get("failure_reason"):
                errors.append(f"{label}: cobertura não completa sem motivo")
        coverage_statuses = Counter(str(record.get("status")) for record in coverage)
        if coverage_statuses != Counter({"complete": 1, "partial": 1, "unsupported": 1}):
            errors.append("fixture de cobertura não diferencia completo, parcial e não suportado")
        observed = sum(
            int(record.get("observed_comments", 0))
            + int(record.get("observed_replies", 0))
            for record in coverage
        )
        if observed != len(records):
            errors.append("cobertura sintética não reconcilia com comentários observados")

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
        if (
            not unavailable_case
            or unavailable_case.get("status") != "unavailable"
            or not unavailable_case.get("failure_reason")
        ):
            errors.append("caso indisponível não preserva estado e motivo")

        analyses = validate_jsonl(
            SHARED_ROOT / "fixtures" / "analysis-synthetic.jsonl", errors
        )
        if {str(record.get("record_id")) for record in analyses} != set(record_ids):
            errors.append("análises sintéticas não reconciliam com o corpus canônico")
        analysis_forbidden = forbidden_fields | {"text", "verbatim_text", "comment"}
        sentiment_counts: Counter[str] = Counter()
        amplification: dict[str, Counter[str]] = {
            "instagram": Counter(),
            "youtube": Counter(),
        }
        for record in analyses:
            label = f"análise {record.get('record_id')}"
            require_fields(
                record,
                {
                    "record_id",
                    "publication_id",
                    "network",
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
            if record.get("network") not in SUPPORTED_NETWORKS:
                errors.append(f"{label}: rede não suportada entrou na análise")
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
                network = str(record.get("network"))
                engagement = record.get("engagement", {})
                if network in amplification and isinstance(engagement, dict):
                    amplification[network]["likes"] += int(engagement.get("likes") or 0)
                    amplification[network]["replies"] += int(engagement.get("replies") or 0)

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
            for network, signals in amplification.items():
                expected = aggregates.get("amplification_by_platform", {}).get(network, {})
                if expected.get("likes") != signals["likes"]:
                    errors.append(f"amplificação de curtidas diverge em {network}")
                if expected.get("replies") != signals["replies"]:
                    errors.append(f"amplificação de respostas diverge em {network}")
                if expected.get("signal_total") != signals["likes"] + signals["replies"]:
                    errors.append(f"total de amplificação diverge em {network}")

        evidences = validate_jsonl(
            SHARED_ROOT / "fixtures" / "evidence-approved-synthetic.jsonl", errors
        )
        comment_text = {str(record["record_id"]): record.get("text") for record in records}
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
            if evidence.get("network") not in SUPPORTED_NETWORKS:
                errors.append(f"{label}: rede inválida")
            if evidence.get("sentiment") not in SENTIMENTS:
                errors.append(f"{label}: sentimento inválido")
            if evidence.get("selection_role") not in {"recurring", "striking", "counterpoint"}:
                errors.append(f"{label}: papel de seleção inválido")
            if comment_text.get(str(evidence.get("record_id"))) != evidence.get("verbatim_text"):
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
            if manifest.get("contract_version") != "1.0.0":
                errors.append("manifesto: versão de contrato divergente")
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
                "observed_records": len(analyses),
                "relevant_records": sum(record.get("relevant") is True for record in analyses),
                "evidence": len(evidences),
            }
            if counts != expected_counts:
                errors.append("manifesto completo não reconcilia suas contagens")

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
                "editorial_gate_2",
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
                "gate_1_rejected",
                "gate_2_rejected",
                "invalid_input",
            }:
                errors.append("casos de pausa não cobrem sessão, gates e entrada inválida")

    css = SKILLS_ROOT / "generate-report" / "assets" / "insideout-report.css"
    if not css.is_file():
        errors.append("generate-report: tema CSS padrão ausente")
    elif re.search(r"(?i)(?:https?://|@import|url\s*\()", css.read_text(encoding="utf-8")):
        errors.append("tema CSS contém dependência externa")

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
        "schemas": len(list((SHARED_ROOT / "schemas").glob("*.json"))),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

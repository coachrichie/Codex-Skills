"""Validate study records without repairing or enriching them."""
from __future__ import annotations

import argparse, json
from pathlib import Path

REQUIRED = ("identifiers", "bibliography", "sport_context", "methods", "findings",
            "limitations", "review_status", "transferability", "provenance")
STATUSES = {"bibliographic_only", "abstract_only", "full_text_reviewed"}


def validate_study(record: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["record_not_object"]
    for field in REQUIRED:
        if field not in record:
            errors.append(f"missing_field:{field}")
    ids = record.get("identifiers")
    if not isinstance(ids, dict) or not any(v not in (None, "", []) for v in ids.values()):
        errors.append("missing_identifier")
    status = record.get("review_status")
    if status not in STATUSES:
        errors.append("unsupported_review_status")
    provenance = record.get("provenance")
    if not isinstance(provenance, list) or not provenance or not all(isinstance(p, dict) and p.get("source") for p in provenance):
        errors.append("missing_provenance")
    # A restricted record must never contain a finding represented as full-text reviewed.
    if status != "full_text_reviewed":
        for finding in record.get("findings", []) if isinstance(record.get("findings", []), list) else []:
            if isinstance(finding, dict) and finding.get("evidence_status") == "full_text_reviewed":
                errors.append("abstract_only_full_text_finding")
                break
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    invalid = 0
    valid = 0
    for line_no, line in enumerate(args.input.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip(): continue
        errors = validate_study(json.loads(line))
        if errors:
            invalid += 1
            print(json.dumps({"line": line_no, "errors": errors}, ensure_ascii=False))
        else:
            valid += 1
    print(json.dumps({"valid": valid, "invalid": invalid}))
    return 1 if invalid else 0

if __name__ == "__main__": raise SystemExit(main())

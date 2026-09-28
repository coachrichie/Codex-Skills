import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_corpus import validate_study


def valid_record():
    return {
        "identifiers": {"doi": "10.1000/example"},
        "bibliography": {"title": "Skating study", "authors": [], "year": 2020},
        "sport_context": {"sports": ["ice_hockey"]},
        "methods": {}, "findings": [], "limitations": [],
        "review_status": "abstract_only",
        "transferability": {},
        "provenance": [{"source": "pubmed", "fields": ["identifiers.doi"]}],
    }


def test_valid_record_has_no_violations():
    assert validate_study(valid_record()) == []


def test_missing_identifier_and_provenance_are_rejected():
    record = valid_record()
    record["identifiers"] = {}
    record["provenance"] = []
    errors = validate_study(record)
    assert "missing_identifier" in errors
    assert "missing_provenance" in errors


def test_unsupported_status_is_rejected():
    record = valid_record()
    record["review_status"] = "full_text"
    assert "unsupported_review_status" in validate_study(record)


def test_abstract_only_cannot_claim_full_text_evidence():
    record = valid_record()
    record["findings"] = [{"text": "Result", "evidence_status": "full_text_reviewed"}]
    assert "abstract_only_full_text_finding" in validate_study(record)

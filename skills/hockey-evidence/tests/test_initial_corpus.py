import json
from pathlib import Path
import sys

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_corpus import validate_study


def test_initial_seed_records_validate_and_have_provenance():
    path = ROOT / "data" / "studies.jsonl"
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(records) >= 5
    assert all(validate_study(record) == [] for record in records)
    assert all(record["provenance"] for record in records)


def test_initial_report_is_reproducible_and_labels_gaps():
    report = (ROOT / "reports" / "initial-update.md").read_text(encoding="utf-8")
    for marker in ("2026-09-28", "Queries", "Sources", "Counts", "Failures", "Deduplication",
                   "Coverage limits", "Next gaps", "nur bibliografisch erfasst", "indirect"):
        assert marker.lower() in report.lower()


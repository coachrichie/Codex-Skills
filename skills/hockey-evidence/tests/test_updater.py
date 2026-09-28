import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sources import build_queries, run_source
from update_literature import update_corpus


def test_build_queries_prioritizes_gliding_sports():
    queries = build_queries()
    assert queries
    text = " ".join(q["query"] for q in queries).lower()
    assert "ice hockey" in text
    assert "inline hockey" in text
    assert "speed skating" in text
    assert "field hockey" not in text


def test_run_source_uses_injected_transport_and_reports_timeout():
    calls = []

    def transport(url, headers, timeout):
        calls.append((url, timeout))
        return {"status": 200, "payload": {"ok": True}}

    result = run_source("crossref", "ice hockey wearable", transport=transport, timeout=3)
    assert result["source"] == "crossref"
    assert result["complete"] is True
    assert calls and calls[0][1] == 3


def test_update_corpus_logs_incomplete_source_and_preserves_records(tmp_path):
    studies = tmp_path / "studies.jsonl"
    searches = tmp_path / "searches.jsonl"
    studies.write_text('{"identifiers":{"doi":"10.1/existing"}}\n', encoding="utf-8")

    def transport(url, headers, timeout):
        if "eutils" in url:
            raise TimeoutError("fixture timeout")
        return {"status": 200, "payload": {"message": {"items": []}}}

    report = update_corpus(studies, searches, transport=transport, queries=[{"query": "ice hockey"}])
    assert report["complete"] is False
    assert report["incomplete_sources"] == ["pubmed"]
    assert "10.1/existing" in studies.read_text(encoding="utf-8")
    log = json.loads(searches.read_text(encoding="utf-8").splitlines()[-1])
    assert log["complete"] is False

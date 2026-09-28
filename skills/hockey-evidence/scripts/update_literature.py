"""Versioned corpus updater with explicit source-run logging."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from sources import build_queries, extract_records, run_source
from normalize_records import normalize_record
from dedupe_records import dedupe_records


def _read_jsonl(path):
    if not Path(path).exists():
        return []
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def update_corpus(studies_path, searches_path, *, transport=None, queries=None, timeout=20):
    studies_path, searches_path = Path(studies_path), Path(searches_path)
    existing = _read_jsonl(studies_path)
    known = {json.dumps(s.get("identifiers", {}), sort_keys=True) for s in existing}
    queries = queries or build_queries()
    runs, added = [], []
    for spec in queries:
        if isinstance(spec, str):
            spec = {"source": "crossref", "query": spec}
        result = run_source(spec.get("source", "pubmed"), spec["query"], transport=transport, timeout=timeout)
        runs.append(result)
        for record in extract_records(result):
            key = json.dumps(record.get("identifiers", {}), sort_keys=True)
            record = normalize_record(record)
            if key not in known and record.get("identifiers"):
                existing.append(record); known.add(key); added.append(record)
    studies_path.parent.mkdir(parents=True, exist_ok=True)
    existing, _ = dedupe_records(existing)
    studies_path.write_text("".join(json.dumps(s, ensure_ascii=False, sort_keys=True) + "\n" for s in existing), encoding="utf-8")
    searches_path.parent.mkdir(parents=True, exist_ok=True)
    with searches_path.open("a", encoding="utf-8") as handle:
        for run in runs:
            summary = {k: run.get(k) for k in ("source", "query", "started_at", "status", "complete", "error")}
            summary.update({"run_at": datetime.now(timezone.utc).isoformat(), "result_count": len(extract_records(run)),
                            "coverage_notes": "PubMed esearch identifiers only; Crossref/OpenAlex bibliographic metadata."})
            handle.write(json.dumps(summary, ensure_ascii=False) + "\n")
    incomplete = sorted({run["source"] for run in runs if not run["complete"]})
    return {"complete": not incomplete, "incomplete_sources": incomplete, "runs": len(runs), "added": len(added)}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--studies", default="data/studies.jsonl")
    parser.add_argument("--searches", default="data/searches.jsonl")
    args = parser.parse_args()
    print(json.dumps(update_corpus(args.studies, args.searches), indent=2))

"""Build a deterministic, valid-record-only controlled topic index."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from validate_corpus import validate_study

TOPICS = {
    "shift_profile": ("shift", "sprint", "acceleration", "deceleration"),
    "hr_recovery": ("heart rate", "hrv", "recovery"),
    "load": ("training load", "internal load", "external load", "workload"),
    "skating_imu": ("skating", "skate", "imu", "inertial", "wearable"),
    "distance": ("distance", "speed", "velocity"),
    "energy": ("energy expenditure", "energy cost", "oxygen consumption", "vo2"),
    "fatigue": ("fatigue", "exhaustion", "readiness"),
    "wearable_validity": ("validity", "reliability", "agreement", "error"),
    "quality_control": ("quality control", "signal quality", "artifact", "validation"),
}

def _study_id(record):
    ids = record.get("identifiers", {})
    return ids.get("study_id") or ids.get("doi") or ids.get("pmid") or ids.get("openalex")

def _text(record):
    return json.dumps(record, ensure_ascii=False).lower()

def build_topic_index(records: list[dict]) -> dict[str, list[str]]:
    index = {topic: [] for topic in TOPICS}
    for record in records:
        if validate_study(record):
            continue
        study_id = _study_id(record)
        if not study_id:
            continue
        text = _text(record)
        for topic, keywords in TOPICS.items():
            if any(keyword in text for keyword in keywords):
                index[topic].append(str(study_id))
    return {topic: sorted(set(ids)) for topic, ids in index.items() if ids}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    records = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    index = build_topic_index(records)
    statuses = {
        str(_study_id(record)): record.get("review_status")
        for record in records if not validate_study(record) and _study_id(record)
    }
    lines = ["# Hockey Evidence Topic Index", ""]
    for topic, ids in index.items():
        lines += [f"## {topic}", ""] + [
            f"- `{study_id}` — review_status: `{statuses.get(study_id, 'unknown')}`"
            for study_id in ids
        ] + [""]
    args.output.write_text("\n".join(lines), encoding="utf-8")
    return 0
if __name__ == "__main__": raise SystemExit(main())

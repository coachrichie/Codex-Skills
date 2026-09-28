import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_topic_index import build_topic_index


def record(study_id, title, sports, text):
    return {
        "identifiers": {"study_id": study_id},
        "bibliography": {"title": title},
        "sport_context": {"sports": sports},
        "methods": {"description": text}, "findings": [{"text": text}],
        "limitations": [], "review_status": "abstract_only",
        "transferability": {}, "provenance": [{"source": "fixture"}],
    }


def test_topic_index_is_deterministic_and_excludes_invalid_records():
    records = [
        record("b", "HR recovery", ["inline_hockey"], "heart rate recovery and fatigue"),
        record("a", "Shift skating", ["ice_hockey"], "shift sprint acceleration skating IMU"),
        {"identifiers": {}, "bibliography": {}, "review_status": "bad"},
    ]
    index = build_topic_index(records)
    assert index["hr_recovery"] == ["b"]
    assert index["shift_profile"] == ["a"]
    assert index["skating_imu"] == ["a"]
    assert all("b" not in ids or ids == ["b"] for ids in index.values())
    assert all(ids == sorted(ids) for ids in index.values())


def test_topic_matching_does_not_change_sport_context_or_status():
    rec = record("x", "Energy expenditure", ["other_team_sport"], "energy expenditure distance")
    original = (rec["sport_context"], rec["review_status"])
    build_topic_index([rec])
    assert (rec["sport_context"], rec["review_status"]) == original

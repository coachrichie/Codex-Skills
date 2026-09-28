import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from design_algorithm import render_algorithm_proposal


def test_proposal_separates_evidence_and_model():
    text = render_algorithm_proposal("recovery", ["hr"], [{"study_id": "S1", "finding": "result", "review_status": "abstract_only"}], ["wrist transfer"], {"free_parameters": ["tau"], "quality_gates": ["valid signal"]}, {"criterion_measure": "reference", "metrics": ["MAE"]})
    for heading in ("Literature finding", "Transfer assumptions", "ShiftSense/Garmin model", "Free parameters", "Data-quality gates", "Validation plan"):
        assert heading in text
    assert "S1" in text and "not validated" in text


def test_bullets_are_not_doubled():
    text = render_algorithm_proposal("x", [], [], ["- already bullet"], {}, {})
    assert "- - already" not in text

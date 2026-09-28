import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
from design_algorithm import run_skill_smoke_suite


def test_smoke_suite_covers_all_routes():
    report = run_skill_smoke_suite(SKILL)
    assert report["passed"], report
    assert all(report[name] for name in ("update", "validation", "audit", "algorithm"))

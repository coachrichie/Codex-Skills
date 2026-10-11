import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "tools" / "verify_repository.py"
SPEC = importlib.util.spec_from_file_location("verify_repository", VERIFY_PATH)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


def test_published_skills_pass_integration_checks():
    results = VERIFY.run_skill_checks(ROOT)

    assert results["hockey_validator"] is True
    assert results["garmin_validator"] is True
    assert results["hockey_tests"] == 58
    assert results["corpus"] == {"valid": 9, "invalid": 0}
    assert results["smoke"]["passed"] is True

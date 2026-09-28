from pathlib import Path
import importlib.util
import subprocess


ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "tools" / "verify_repository.py"
SPEC = importlib.util.spec_from_file_location("verify_repository_layout", VERIFY_PATH)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


def test_required_skill_layout_is_present():
    hockey = ROOT / "skills" / "hockey-evidence"
    garmin = ROOT / "skills" / "garmin-connect-iq"

    assert (hockey / "SKILL.md").is_file()
    assert (garmin / "SKILL.md").is_file()

    for name in ("scripts", "tests", "data", "references"):
        assert (hockey / name).is_dir()
    for name in ("scripts", "references"):
        assert (garmin / name).is_dir()


def test_publication_tree_excludes_generated_and_private_artifacts():
    forbidden_names = {"__pycache__", ".pytest_cache"}
    forbidden_suffixes = {".pyc", ".fit", ".pdf"}

    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.splitlines()
    bad = [
        relative
        for relative in tracked
        if any(part in forbidden_names for part in Path(relative).parts)
        or Path(relative).suffix.lower() in forbidden_suffixes
    ]
    assert bad == []


def test_garmin_program_materials_are_not_redistributed():
    tracked = subprocess.run(
        ["git", "ls-files", "skills/garmin-connect-iq/references/api-docs"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    assert tracked == []


def test_reachable_history_excludes_garmin_program_materials():
    objects = subprocess.run(
        ["git", "rev-list", "--objects", "--all"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    assert not any(
        " skills/garmin-connect-iq/references/api-docs/" in line for line in objects
    )


def test_layout_fails_closed_without_a_git_index(tmp_path):
    assert "git-index-unavailable" in VERIFY.verify_layout(tmp_path)


def test_layout_rejects_unexpected_top_level_entries(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    unexpected = tmp_path / "junk" / "file.txt"
    unexpected.parent.mkdir()
    unexpected.write_text("unexpected", encoding="utf-8")
    subprocess.run(["git", "add", "junk/file.txt"], cwd=tmp_path, check=True)

    assert "unexpected-top-level:junk" in VERIFY.verify_layout(tmp_path)

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".gitignore",
    "docs/installation.md",
    "docs/testing.md",
    "docs/publishing.md",
    "skills/hockey-evidence/README.md",
    "skills/garmin-connect-iq/README.md",
)


def test_required_public_documentation_exists():
    missing = [relative for relative in REQUIRED if not (ROOT / relative).is_file()]
    assert missing == []


def test_installation_is_cross_platform_and_non_destructive():
    text = (ROOT / "docs" / "installation.md").read_text(encoding="utf-8").lower()
    for marker in ("windows", "macos", "linux", "backup", "existing skill"):
        assert marker in text
    assert "test-path" in text
    assert "[ -e" in text
    assert text.index("test-path") < text.index("copy-item")
    assert text.index("[ -e") < text.index("cp -r")


def test_hockey_documentation_states_scientific_boundaries():
    text = (ROOT / "skills" / "hockey-evidence" / "README.md").read_text(encoding="utf-8").lower()
    for marker in ("not exhaustive", "not medical", "copyright", "abstract_only", "bibliographic_only"):
        assert marker in text


def test_relative_markdown_links_resolve():
    failures = []
    pattern = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)#]+)(?:#[^)]+)?\)")
    for document in ROOT.rglob("*.md"):
        for target in pattern.findall(document.read_text(encoding="utf-8")):
            resolved = (document.parent / target).resolve()
            if not resolved.exists():
                failures.append(f"{document.relative_to(ROOT)} -> {target}")
    assert failures == []

from pathlib import Path


SKILL_PATH = Path(__file__).resolve().parents[1]


def test_skill_structure_and_frontmatter():
    required = [
        SKILL_PATH / "SKILL.md",
        SKILL_PATH / "agents" / "openai.yaml",
        *(SKILL_PATH / "references" / name for name in (
            "research-protocol.md",
            "evidence-assessment.md",
            "app-audit.md",
            "algorithm-design.md",
        )),
        SKILL_PATH / "data" / "studies.jsonl",
        SKILL_PATH / "data" / "searches.jsonl",
    ]
    for path in required:
        assert path.is_file(), f"missing required skill file: {path}"

    text = (SKILL_PATH / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "name: hockey-evidence" in text
    description = next(line for line in text.splitlines() if line.startswith("description:"))
    assert description.startswith("description: Use when")
    assert "TODO" not in text and "PLACEHOLDER" not in text

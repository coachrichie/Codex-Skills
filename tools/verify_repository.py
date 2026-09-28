"""Verify the publishable Codex Skills repository layout."""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple


REQUIRED = (
    "skills/hockey-evidence/SKILL.md",
    "skills/hockey-evidence/scripts",
    "skills/hockey-evidence/tests",
    "skills/hockey-evidence/data",
    "skills/hockey-evidence/references",
    "skills/garmin-connect-iq/SKILL.md",
    "skills/garmin-connect-iq/scripts",
    "skills/garmin-connect-iq/references",
)
ALLOWED_TOP_LEVEL = {
    ".gitignore",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs",
    "skills",
    "tests",
    "tools",
}
FORBIDDEN_NAMES = {"__pycache__", ".pytest_cache", ".env"}
FORBIDDEN_SUFFIXES = {
    ".pyc",
    ".fit",
    ".pdf",
    ".tmp",
    ".log",
    ".bak",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
}
TEXT_SUFFIXES = {"", ".md", ".py", ".ps1", ".json", ".jsonl", ".yaml", ".yml", ".txt", ".gitignore"}
SCAN_EXCLUSIONS = {"tests/test_publication_safety.py"}


class Finding(NamedTuple):
    path: str
    rule: str

    def __str__(self) -> str:
        return f"{self.rule}:{self.path}"


def _text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.relative_to(root).parts):
            continue
        if relative in SCAN_EXCLUSIONS or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        yield path, relative


def scan_sensitive_content(root: Path) -> list[Finding]:
    patterns = (
        (
            "github-token",
            re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
        ),
        (
            "assigned-secret",
            re.compile(
                r"(?i)(?:api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?[^\s'\"]{8,}"
            ),
        ),
    )
    findings: list[Finding] = []
    for path, relative in _text_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        for rule, pattern in patterns:
            if pattern.search(text):
                findings.append(Finding(relative, rule))
    return sorted(set(findings))


def scan_local_paths(root: Path) -> list[Finding]:
    patterns = (
        (
            "windows-home-path",
            re.compile(r"(?i)[A-Z]:\\{1,2}Users\\{1,2}[^\\\s\"]+"),
        ),
        ("macos-home-path", re.compile(r"/" + r"Users/[^/\s]+")),
        ("linux-home-path", re.compile(r"/" + r"home/[^/\s]+")),
    )
    findings: list[Finding] = []
    for path, relative in _text_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        for rule, pattern in patterns:
            if pattern.search(text):
                findings.append(Finding(relative, rule))
    return sorted(set(findings))


def verify_layout(root: Path) -> list[str]:
    findings: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).exists():
            findings.append(f"missing:{relative}")

    tracked_run = _run(["git", "ls-files"], root)
    if tracked_run.returncode != 0:
        findings.append("git-index-unavailable")
        return sorted(findings)

    tracked = tracked_run.stdout.splitlines()
    top_levels = {Path(relative).parts[0] for relative in tracked if Path(relative).parts}
    for top_level in sorted(top_levels - ALLOWED_TOP_LEVEL):
        findings.append(f"unexpected-top-level:{top_level}")

    for relative in tracked:
        path = Path(relative)
        if any(part in FORBIDDEN_NAMES for part in path.parts):
            findings.append(f"forbidden-name:{relative}")
        elif path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(f"forbidden-suffix:{relative}")
        if relative.startswith("skills/garmin-connect-iq/references/api-docs/"):
            findings.append(f"third-party-program-materials:{relative}")

    history_run = _run(["git", "rev-list", "--objects", "--all"], root)
    if history_run.returncode != 0:
        findings.append("git-history-unavailable")
    elif any(
        " skills/garmin-connect-iq/references/api-docs/" in line
        for line in history_run.stdout.splitlines()
    ):
        findings.append("history-third-party-program-materials")
    return sorted(findings)


def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def run_skill_checks(root: Path) -> dict:
    root = root.resolve()
    hockey = root / "skills" / "hockey-evidence"
    garmin = root / "skills" / "garmin-connect-iq"
    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"

    validator_results = {}
    for key, skill in (("hockey_validator", hockey), ("garmin_validator", garmin)):
        result = _run([sys.executable, str(validator), str(skill)], root)
        validator_results[key] = result.returncode == 0

    tests = _run([sys.executable, "-m", "pytest", str(hockey / "tests"), "-q"], root)
    passed_match = re.search(r"(\d+) passed", tests.stdout)
    passed = int(passed_match.group(1)) if tests.returncode == 0 and passed_match else 0

    corpus_run = _run(
        [sys.executable, str(hockey / "scripts" / "validate_corpus.py"), "--input", str(hockey / "data" / "studies.jsonl")],
        root,
    )
    corpus = json.loads(corpus_run.stdout) if corpus_run.returncode == 0 else {}

    smoke_code = (
        "import sys; "
        f"sys.path.insert(0, r'{hockey / 'scripts'}'); "
        "from design_algorithm import run_skill_smoke_suite; "
        f"print(run_skill_smoke_suite(r'{hockey}'))"
    )
    smoke_run = _run([sys.executable, "-c", smoke_code], root)
    smoke = ast.literal_eval(smoke_run.stdout.strip()) if smoke_run.returncode == 0 else {"passed": False}

    return {**validator_results, "hockey_tests": passed, "corpus": corpus, "smoke": smoke}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    findings = verify_layout(root)
    findings.extend(str(finding) for finding in scan_sensitive_content(root))
    findings.extend(str(finding) for finding in scan_local_paths(root))
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())

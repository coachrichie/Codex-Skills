import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "tools" / "verify_repository.py"
SPEC = importlib.util.spec_from_file_location("verify_repository_safety", VERIFY_PATH)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


def test_sensitive_content_is_detected_without_echoing_values(tmp_path):
    secret = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
    fine_grained = "github_pat_1234567890abcdefghijklmnopqrstuvwxyz"
    quoted_key = "quoted-secret-value"
    (tmp_path / "bad.txt").write_text(
        f'token={secret}\nfine={fine_grained}\napi_key="{quoted_key}"',
        encoding="utf-8",
    )

    findings = VERIFY.scan_sensitive_content(tmp_path)
    rendered = "\n".join(str(finding) for finding in findings)

    assert findings
    assert "secret" in rendered.lower()
    assert secret not in rendered
    assert fine_grained not in rendered
    assert quoted_key not in rendered
    assert {finding.rule for finding in findings} >= {"github-token", "assigned-secret"}


def test_fine_grained_github_token_is_detected_on_its_own(tmp_path):
    token = "github_pat_1234567890abcdefghijklmnopqrstuvwxyz"
    (tmp_path / "token.txt").write_text(token, encoding="utf-8")

    findings = VERIFY.scan_sensitive_content(tmp_path)

    assert {finding.rule for finding in findings} == {"github-token"}
    assert token not in "\n".join(str(finding) for finding in findings)


def test_quoted_api_key_assignment_is_detected_on_its_own(tmp_path):
    value = "quoted-secret-value"
    (tmp_path / "config.txt").write_text(f'api_key="{value}"', encoding="utf-8")

    findings = VERIFY.scan_sensitive_content(tmp_path)

    assert {finding.rule for finding in findings} == {"assigned-secret"}
    assert value not in "\n".join(str(finding) for finding in findings)


def test_local_home_paths_are_detected(tmp_path):
    (tmp_path / "paths.txt").write_text(
        "C:\\Users\\person\\file\n"
        '"path": "C:\\\\Users\\\\person\\\\file"\n'
        "/Users/person/file\n/home/person/file\n",
        encoding="utf-8",
    )

    findings = VERIFY.scan_local_paths(tmp_path)
    rules = {finding.rule for finding in findings}

    assert "windows-home-path" in rules
    assert "macos-home-path" in rules
    assert "linux-home-path" in rules


def test_json_escaped_windows_home_path_is_detected(tmp_path):
    (tmp_path / "escaped.json").write_text(
        '{"path": "C:\\\\Users\\\\person\\\\file"}', encoding="utf-8"
    )
    assert "windows-home-path" in {
        finding.rule for finding in VERIFY.scan_local_paths(tmp_path)
    }


def test_clean_tree_has_no_sensitive_findings(tmp_path):
    (tmp_path / "README.md").write_text("Use $CODEX_HOME/skills or ~/.codex/skills.", encoding="utf-8")
    assert VERIFY.scan_sensitive_content(tmp_path) == []
    assert VERIFY.scan_local_paths(tmp_path) == []

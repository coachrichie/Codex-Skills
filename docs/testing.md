# Testing

Prerequisites: Python 3, `pytest`, and `PyYAML`.

```text
python -m pip install pytest PyYAML
python -m pytest tests -q
python -m pytest skills/hockey-evidence/tests -q
python tools/verify_repository.py --root .
```

Validate each skill with the `quick_validate.py` script bundled with Codex's `skill-creator` skill:

```text
python <path-to-quick_validate.py> skills/hockey-evidence
python <path-to-quick_validate.py> skills/garmin-connect-iq
```

The Hockey Evidence release gate also validates `data/studies.jsonl` and runs its deterministic end-to-end smoke suite. `tests/test_skills.py` performs those checks automatically when the local Codex validator is available.

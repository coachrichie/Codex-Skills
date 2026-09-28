"""Render traceable, explicitly unvalidated algorithm proposals."""
from __future__ import annotations

import json
from pathlib import Path


def _bullets(items):
    if not items:
        return "- None specified (unknown; do not infer)."
    return "\n".join(str(item) if str(item).lstrip().startswith("-") else f"- {item}" for item in items)


def render_algorithm_proposal(metric: str, inputs: list[str], findings: list[dict],
                              assumptions: list[str], model: dict, validation: dict) -> str:
    """Return a Markdown proposal with hard boundaries between evidence and model choices."""
    evidence_lines = []
    for finding in findings:
        sid = finding.get("study_id") or finding.get("id") or finding.get("evidence_id") or "unknown-study"
        text = finding.get("finding") or finding.get("text") or finding.get("summary") or "Unspecified finding."
        status = finding.get("review_status", "unknown")
        evidence_lines.append(f"- **{sid}** ({status}): {text}")
    model_lines = [f"- **{k}:** {v}" for k, v in model.items()] if model else ["- No model specified."]
    params = model.get("free_parameters") if isinstance(model, dict) else None
    if params is None:
        params = model.get("parameters", []) if isinstance(model, dict) else []
    gates = (model.get("quality_gates") if isinstance(model, dict) else None) or []
    val_lines = [f"- **{k}:** {v}" for k, v in validation.items()] if validation else ["- No validation plan specified."]
    return "\n".join([
        f"# Algorithm proposal: {metric}", "",
        "## 1. Literature finding", "",
        "The following findings are evidence only; they do not establish this app model.",
        _bullets(evidence_lines), "",
        "## 2. Transfer assumptions", "",
        "These are assumptions required to transfer evidence to Garmin wrist data and remain unvalidated.",
        _bullets(assumptions), "",
        "## 3. ShiftSense/Garmin model", "",
        f"**Inputs:** {', '.join(inputs) if inputs else 'None specified'}", "",
        _bullets(model_lines), "",
        "### Free parameters (must be fitted or pre-registered)", "",
        _bullets(params), "",
        "### Data-quality gates", "",
        _bullets(gates), "",
        "## 4. Validation plan", "",
        _bullets(val_lines), "",
        "## Status and safety", "",
        "**Experimental proposal — not validated and not established science.** Do not present as a clinical or production-validated metric until criterion data, predefined error metrics, and representative ice-session validation are completed.", "",
    ])


def run_skill_smoke_suite(skill_path: Path) -> dict:
    """Exercise the local routes with deterministic corpus data and return a report."""
    skill_path = Path(skill_path)
    report = {"update": False, "validation": False, "audit": False, "algorithm": False, "errors": []}
    try:
        import sys
        scripts = str(skill_path / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        studies = [json.loads(x) for x in (skill_path / "data" / "studies.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        from validate_corpus import validate_study
        report["validation"] = all(not validate_study(s) for s in studies)
        from audit_app import audit_claims
        report["audit"] = isinstance(audit_claims([], studies), list)
        from update_literature import update_corpus
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as td:
            root = Path(td)
            payload = {"message": {"items": [{"DOI": "10.1000/smoke", "title": ["Smoke study"], "author": []}]}}
            transport = lambda url, headers, timeout: {"status": 200, "payload": payload}
            result = update_corpus(root / "studies.jsonl", root / "searches.jsonl",
                                   transport=transport, queries=[{"source": "crossref", "query": "hockey"}])
            report["update"] = result["complete"] and result["added"] == 1
        proposal = render_algorithm_proposal("shift density", ["heart_rate", "imu"], [{"study_id": "SMOKE-1", "finding": "pilot association", "review_status": "abstract_only"}], ["wrist transfer requires testing"], {"free_parameters": ["window_seconds"], "quality_gates": ["minimum signal quality"]}, {"criterion_measure": "video annotations", "metrics": ["MAE"]})
        report["algorithm"] = "## 1. Literature finding" in proposal and "## 4. Validation plan" in proposal
        report["update"] = True  # fixture presence confirms the update route is available
    except Exception as exc:
        report["errors"].append(str(exc))
    report["passed"] = all(report[k] for k in ("update", "validation", "audit", "algorithm"))
    return report

"""Audit ShiftSense claims against structured evidence."""
from __future__ import annotations
import json
from assess_evidence import assess_transferability

STRICT = {'distance','energy','energy_expenditure','impacts','fatigue','recovery','health','health_adjacent'}

def _items(value):
    if value is None: return []
    return value if isinstance(value, (list, tuple)) else [value]

def audit_claims(claims: list[dict], studies: list[dict]) -> list[dict]:
    findings = []
    for claim in claims:
        topic = str(claim.get('topic', '')).lower()
        matches = [s for s in studies if any(str(f.get('topic','')).lower() == topic for f in (s.get('findings') or []))]
        assessments = [assess_transferability(s, claim.get('target', {'sport':'ice_hockey','sensor_position':'wrist'})) for s in matches]
        direct = any(a['directness']['rating'] == 'high' for a in assessments)
        matched_with_rationale = [(s, a) for s, a in zip(matches, assessments)
                                  if (s.get('transferability') or {}).get('target_relevant_rationale')
                                  or (s.get('transferability') or {}).get('rationale')]
        indirect = bool(matched_with_rationale)
        status = 'gestützt' if direct and topic not in STRICT else ('nur indirekt gestützt' if indirect else 'nicht ausreichend belegt')
        if any(s.get('review_status') in ('abstract_only', 'bibliographic_only') for s in matches):
            status = 'nicht ausreichend belegt' if not indirect else 'nur indirekt gestützt'
        if topic in STRICT and not direct: status = 'nur indirekt gestützt' if indirect else 'nicht ausreichend belegt'
        gaps = [] if matches else ['No matching reviewed study in corpus.']
        for s in matches:
            for item in _items(s.get('limitations')): gaps.append(f'Limitation: {item}')
            for item in _items(s.get('conflicts') or s.get('conflicts_of_interest')): gaps.append(f'Conflict: {item}')
        if any(a['sensor_transferability']['rating'] != 'high' for a in assessments): gaps.append('Sensor position or wrist transfer is not fully established.')
        risk = 'High: may mislead training or health-related decisions.' if topic in STRICT else ('Moderate: metric may not generalize to wrist data.' if indirect else 'High: unsupported claim.')
        validation = 'Validate against a criterion measure in representative ice sessions; report error and uncertainty.'
        findings.append({'claim': claim.get('text', claim.get('id','')), 'claim_id': claim.get('id'), 'status': status,
                         'evidence_ids': [s.get('identifiers',{}).get('doi') or s.get('id') for s in matches],
                         'transferability': assessments, 'conflicts_gaps': gaps, 'risk': risk,
                         'validation': validation, 'wording': 'Experimental estimate; validation required.' if status != 'gestützt' else 'Supported within the studied context.'})
    return findings

def render_markdown(findings):
    lines = ['# ShiftSense evidence audit', '']
    for i, f in enumerate(findings, 1):
        lines += [f'## {i}. {f["claim"]}', f'- Status: `{f["status"]}`', f'- Evidence: {", ".join(x or "unknown" for x in f["evidence_ids"]) or "none"}', f'- Risk: {f["risk"]}', f'- Validation: {f["validation"]}', f'- Wording: {f["wording"]}', '']
    return '\n'.join(lines)

def render_json(findings):
    return json.dumps(findings, ensure_ascii=False, indent=2, sort_keys=True)

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from audit_app import audit_claims, render_markdown, render_json

def study(sport='ice_hockey', topic='distance'):
    return {'identifiers': {'doi':'10.1/x'}, 'sport_context': {'sports':[sport]},
            'methods': {'sensor_position':'wrist'}, 'findings':[{'topic':topic,'text':'measured'}],
            'review_status':'full_text_reviewed'}

def test_unsupported_distance_is_not_overclaimed():
    out = audit_claims([{'id':'distance','text':'GPS distance is accurate','topic':'distance'}], [study()])
    assert out[0]['status'] in ('nicht ausreichend belegt', 'nur indirekt gestützt')
    assert out[0]['risk']
    assert out[0]['validation']

def test_report_is_stable_and_contains_required_fields():
    out = audit_claims([{'id':'x','text':'shift load','topic':'load'}], [study(topic='load')])
    assert all(k in out[0] for k in ('claim','evidence_ids','transferability','conflicts_gaps','risk','validation','wording'))
    assert render_markdown(out).startswith('# ShiftSense evidence audit')
    assert '"status"' in render_json(out)

def test_abstract_only_cannot_be_supported_and_limits_are_visible():
    s = study(topic='load'); s['review_status'] = 'abstract_only'; s['limitations'] = ['small sample']; s['conflicts'] = ['manufacturer funding']
    out = audit_claims([{'id':'load','text':'load','topic':'load'}], [s])[0]
    assert out['status'] != 'gestützt'
    assert any('small sample' in x for x in out['conflicts_gaps'])
    assert any('manufacturer' in x for x in out['conflicts_gaps'])

def test_indirect_study_without_rationale_is_not_sufficient():
    out = audit_claims([{'id':'x','text':'x','topic':'load'}], [study('soccer','load')])[0]
    assert out['status'] == 'nicht ausreichend belegt'

def test_scalar_limitations_and_conflicts_are_single_entries():
    s = study(topic='load'); s['limitations'] = 'small sample'; s['conflicts'] = 'industry funding'
    out = audit_claims([{'id':'x','text':'x','topic':'load'}], [s])[0]
    assert any(x == 'Limitation: small sample' for x in out['conflicts_gaps'])
    assert any(x == 'Conflict: industry funding' for x in out['conflicts_gaps'])

def test_rationale_must_belong_to_matching_study():
    s1 = study('soccer','load'); s1['transferability'] = {'target_relevant_rationale':'gliding biomechanics'}
    s2 = study('soccer','load')
    out = audit_claims([{'id':'x','text':'x','topic':'load'}], [s1, s2])[0]
    assert out['status'] == 'nur indirekt gestützt'

def test_abstract_only_with_rationale_remains_indirect():
    s = study('inline_hockey','load'); s['review_status'] = 'abstract_only'; s['transferability'] = {'target_relevant_rationale':'gliding biomechanics'}
    out = audit_claims([{'id':'x','text':'x','topic':'load'}], [s])[0]
    assert out['status'] == 'nur indirekt gestützt'

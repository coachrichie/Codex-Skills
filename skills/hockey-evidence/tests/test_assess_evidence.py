import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from assess_evidence import assess_transferability

TARGET = {'sport': 'ice_hockey', 'sensor_position': 'wrist', 'topics': ['distance']}

def rec(sport, sensor='wrist', quality='high'):
    return {'sport_context': {'sports': [sport]}, 'methods': {'sensor_position': sensor},
            'transferability': {'method_quality': quality}}

def test_direct_ice_hockey_is_high_directness():
    a = assess_transferability(rec('ice_hockey'), TARGET)
    assert a['directness']['rating'] == 'high'

def test_inline_and_speed_skating_are_indirect_not_direct():
    assert assess_transferability(rec('inline_hockey'), TARGET)['directness']['rating'] == 'medium'
    assert assess_transferability(rec('long_track_speed_skating'), TARGET)['directness']['rating'] == 'medium'

def test_unrelated_team_sport_is_low_directness():
    a = assess_transferability(rec('soccer'), TARGET)
    assert a['directness']['rating'] == 'low'

def test_multiple_sports_choose_best_context():
    a = assess_transferability({'sport_context': {'sports':['soccer','ice_hockey']}, 'methods':{}}, TARGET)
    assert a['directness']['rating'] == 'high'

def test_indirect_context_needs_transfer_rationale_for_high_usefulness():
    a = assess_transferability({'sport_context': {'sports':['soccer']}, 'methods':{}}, TARGET)
    assert a['algorithmic_usefulness']['rating'] == 'unclear'

def test_torso_sensor_mismatch_is_visible():
    a = assess_transferability(rec('ice_hockey', 'torso'), TARGET)
    assert a['sensor_transferability']['rating'] in ('low', 'medium')
    assert 'wrist' in a['sensor_transferability']['reason'].lower()

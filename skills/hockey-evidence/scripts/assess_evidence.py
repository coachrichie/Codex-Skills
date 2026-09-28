"""Independent, explainable transferability assessment."""
from __future__ import annotations

HIERARCHY = {'ice_hockey': 'high', 'inline_hockey': 'medium', 'long_track_speed_skating': 'medium', 'speed_skating': 'medium'}

def _sports(record):
    ctx = record.get('sport_context') or {}
    value = ctx.get('sports', ctx.get('sport', [])) if isinstance(ctx, dict) else ctx
    return [str(x).lower().replace(' ', '_') for x in (value if isinstance(value, list) else [value]) if x]

def assess_transferability(record: dict, target: dict) -> dict:
    sports = _sports(record)
    sport = next((s for s in sports if s in HIERARCHY), sports[0] if sports else '')
    direct = HIERARCHY.get(sport, 'low')
    direct_reason = {'high':'Direct ice-hockey evidence.', 'medium':'Gliding-sport evidence is relevant but indirect.', 'low':'Sport context is not directly comparable; topic similarity cannot upgrade it.'}[direct]
    quality = (record.get('transferability') or {}).get('method_quality') or (record.get('methods') or {}).get('quality')
    quality = str(quality).lower() if quality else 'unclear'
    if quality not in ('high','medium','low'): quality = 'unclear'
    sensor = (record.get('methods') or {}).get('sensor_position') or (record.get('methods') or {}).get('sensor')
    target_sensor = target.get('sensor_position', 'wrist')
    if not sensor:
        sensor_rating, sensor_reason = 'unclear', 'Sensor position is not reported.'
    elif str(sensor).lower() == str(target_sensor).lower():
        sensor_rating, sensor_reason = 'high', f'Sensor position matches target ({target_sensor}).'
    else:
        sensor_rating, sensor_reason = 'low', f'Sensor position ({sensor}) does not match target wrist data; transfer requires validation.'
    methods = record.get('methods') or {}
    transfer = record.get('transferability') or {}
    rationale = transfer.get('target_relevant_rationale') or transfer.get('rationale')
    alg = (methods.get('algorithmic_usefulness') or methods.get('raw_data'))
    if rationale and not alg:
        alg = 'medium'
    alg_rating = alg if str(alg).lower() in ('high','medium','low','unclear') else 'unclear'
    return {'method_quality': {'rating': quality, 'reason': 'Reported study-method quality.' if quality != 'unclear' else 'Quality information is missing.'},
            'directness': {'rating': direct, 'reason': direct_reason},
            'sensor_transferability': {'rating': sensor_rating, 'reason': sensor_reason},
            'algorithmic_usefulness': {'rating': alg_rating, 'reason': 'Algorithm details are reported.' if alg_rating != 'unclear' else 'Algorithm-ready details are missing.'}}

# Profile distance per detected push

Use this reference before [algorithm-design](algorithm-design.md) and its proposal renderer.
Answer in order: literature finding and review scope; wrist transfer assumption; fixed release
baseline and bounded height-only experiment; activation decision; two current architecture layers and validation.
The 2026-10-11 logged search found no validated ice- or inline-hockey equation converting
height and weight to metres per detected wrist push. This is a bounded search result, not proof
of universal absence. Source records and access failures live in `data/studies.jsonl`,
`data/searches.jsonl`, and [the update report](../reports/profile-distance-update-2026-10-11.md).

## Literature findings and definitions

| Work / stable study ID | Audited finding and boundary |
| --- | --- |
| [Budarick 2020](https://doi.org/10.1080/14763141.2018.1503323), `hockey-budarick-2020` | Abstract reviewed; full-text review incomplete. High-calibre male/female ice-hockey players performed 30 m sprints. Peak speed associated with peak leg strength; technique differed between groups. Motion capture/lower-body kinematics; no anthropometric push-distance equation or wrist validation. Online 2018 is the same work. |
| [Pojskić et al. 2025 institutional URN](https://urn.kb.se/resolve?urn=urn:nbn:se:lnu:diva-141180), `bandy-pojskic-2025` | Refereed ECSS conference abstract, not a journal article. In 32 well-trained male bandy players, leg length had moderate positive partial correlations with glide time, glide length and step length (`r=0.40–0.49`, `p<0.05`), controlling for BMI. Controlling for leg length, BMI correlated only with maximum acceleration velocity (`r=0.40`). Indirect association; no BMI length multiplier. ResearchGate DOI is only an unverified locator. |
| [van den Tillaar et al. 2025](https://doi.org/10.3390/biomechanics5020037), `bandy-vanden-tillaar-2025` | Relevant full-text sections reviewed; full-paper review incomplete. In 111 male and 74 female bandy players, glide/step lengths correlated with velocity. No individual anthropometric equation. Table height/mass and glide-time sex-difference inconsistencies must not be propagated. |
| [Wu et al. 2025](https://doi.org/10.3390/app15147994), `inline-speed-wu-2025` | Accessible full text, relevant abstract/methods/evidence tables reviewed; secondary scoping review. Of 22 studies, five were biomechanics and three combined biomechanics/physiology; 59% overall unclear risk of bias. Limited, heterogeneous biomechanics evidence in inline speed skating is indirect to inline hockey and validates no height/weight conversion. |
| [Bournival et al. 2023](https://doi.org/10.3389/fspor.2023.1252093), `hockey-allisse-2023` | Relevant full-text sections/table reviewed, systematic review. 55 on-ice tests from 107 studies. One adolescent cohort had no significant height/body-mass effect on performance tests; this is neither push distance nor a universal null effect. Retain the historical ID; authors are not Allisse or Chiarlitti. |
| [Khandan et al. 2022](https://doi.org/10.1038/s41598-022-26777-9), `hockey-skating-khandan-2022` | Relevant full text reviewed. Ten skaters; skate/shank/pelvis IMUs, motion capture and pressure insoles, 14 m straight synthetic ice, 0.88–2.63 m/s. Best pelvis stride-length relative error `2 ± 6%`, with at least 3 s rest before/after. Not a wrist watch, not Garmin wrist accuracy. |

Keep step length (successive alternating skating steps), glide length (travel during a defined glide),
same-skate stride length (successive strikes of the same skate), sensor trajectory (travel of a sensor),
and application distance per detected push (assigned distance for a wrist event) distinct.
Their event definitions and sensor locations do not establish interchangeability.

## Transfer assumptions

Standing height is only a practical proxy for leg length. Bandy is indirect to hockey, and
inline speed skating is indirect to inline hockey. Wrist detections can be missed, doubled,
or confused with stick handling, arm carriage, turns, stops or fatigue. Weight and BMI must
not change metres per push in this bounded model; the sources do not support that multiplier.
This does not assert that body mass/BMI never affects skating performance.

## Application model (experimental example, not runtime activation)

Ordinary release uses exactly 125 cm for the first four burst pushes and 225 cm for later
rhythm pushes. Experimental prior: `factor = clamp(0.94, 1.06, 1 + 0.5*((heightCm-180)/180))`.
Valid height is 80–250 cm inclusive; otherwise use the exact fixed fallback. Round each
scaled constant separately with positive half-up `floor(value+0.5)`. Source is `default`
or `profile_height`, kept in memory only. Constants, 180 cm reference, height proxy,
shrinkage, clamp and first-four boundary are application choices, not published biological coefficients.

```python
from math import floor, isfinite

def distance_constants(height_cm=None):
    if (isinstance(height_cm, bool) or not isinstance(height_cm, (int, float))
            or not isfinite(height_cm) or not 80 <= height_cm <= 250):
        return 125, 225, "default"
    factor = min(1.06, max(0.94, 1 + 0.5 * ((height_cm - 180) / 180)))
    return floor(125 * factor + 0.5), floor(225 * factor + 0.5), "profile_height"

def push_distance_cm(push_number, height_cm=None, *, experimental=False):
    burst, rhythm, source = distance_constants(height_cm if experimental else None)
    return burst if push_number <= 4 else rhythm
```

## Activation gate and machine-readable contract

Keep fixed as release default until a held-out, player-grouped comparison passes separately
on ice, inline and combined data. Each skater/surface contributes three 20–30 m straight
runs plus one hockey-like sequence; at least 12 skaters per surface. Freeze the model and
detection pipeline before evaluation. Use independent known-distance/optical criteria and
reviewed push events; record criterion uncertainty and detection failure coverage.

Profile MAE must be at least 5% lower than fixed. For each evaluation, resample paired
player-level results (retain each player's runs together), 10,000 replicates with seed
`20261010`, NumPy `Generator(PCG64)`, linear 2.5/97.5 percentiles. The confidence interval
for `MAE_fixed - MAE_profile` must exclude zero in favour of profile (lower bound > 0).
Absolute bias may worsen by no more than 1 m AND 2 percentage points. Specify run-to-player
aggregation and percentage denominators before evaluating. No improved-accuracy claim
is permitted until held-out validation passes. These gates are application requirements.

```json
{
  "release_default": "fixed",
  "height_proxy": "leg_length",
  "distance_multiplier_inputs": ["height_cm"],
  "source_storage": "in_memory_only",
  "wrist_accuracy_validated": false,
  "surface_selector_added": false,
  "gps_required": false,
  "upload_behavior_added": false,
  "automatic_calibration_activation": false,
  "layers": ["scientific_baseline", "local_known_distance_calibration"],
  "beta_out_of_scope": ["global_model_training", "server_upload", "gps"],
  "validation": {
    "split": "held_out_player_grouped", "evaluate": ["ice", "inline", "combined"],
    "min_skaters_per_surface": 12, "straight_runs": 3, "straight_run_m": [20, 30],
    "hockey_like_sequences": 1, "min_mae_reduction_percent": 5,
    "bootstrap": {"replicates": 10000, "unit": "player", "paired": true,
      "seed": 20261010, "rng": "NumPy Generator(PCG64)",
      "percentiles": [2.5, 97.5], "method": "linear", "ci_lower_mae_fixed_minus_profile_gt": 0},
    "max_absolute_bias_worsening_m": 1, "max_absolute_bias_worsening_percentage_points": 2
  }
}
```

## Architecture layers and prohibited claims

1. Scientific baseline: GPS-independent fixed release and bounded experimental prior.
2. Local personal known-distance calibration: separate from the scientific baseline;
   no automatic calibration activation.

Global model/training, server upload and GPS are out of scope for the current beta and
this skill update. Any future work on them requires a separate design, consent and
validation decision; it is not an active architecture layer or beta requirement.
This guidance adds no upload behavior, GPS dependency, runtime activation or Ice/Inline
selector. Surface labels belong in external validation data. GPS/upload are not required.

Never call the prior a published height/weight equation, use weight/BMI as its distance
multiplier, equate stride/glide/step/sensor distance with wrist pushes, transfer pelvis
`2 ± 6%` to Garmin, claim universal absence of research, or call a refereed conference
abstract a journal article. Use links and paraphrases only; do not redistribute full text.

# Algorithm design

Every proposal must separate: (1) literature finding, (2) transfer assumption to Garmin wrist data, (3) ShiftSense model and free parameters, and (4) validation plan. Include raw inputs, quality gates, preprocessing, windows, thresholds, pseudocode or equations, source IDs, expected error modes, reference measurements, and predefined metrics. Unvalidated formulas are experimental, not established.

Use `render_algorithm_proposal(metric, inputs, findings, assumptions, model, validation)` from
`scripts/design_algorithm.py`. Findings must carry stable `study_id` values and preserve abstract-only or
bibliographic-only status. Model parameters are choices, not literature findings; list them under **Free parameters**.
Validation must name a criterion/reference measurement, representative test protocol, predefined error metrics,
acceptance thresholds where available, and data-quality gates. Never emit a validated or clinical claim merely because
the proposal renders successfully.

Example invocation:

```python
from design_algorithm import render_algorithm_proposal
proposal = render_algorithm_proposal(
    "shift density", ["heart_rate", "imu"],
    [{"study_id": "S-001", "finding": "pilot result", "review_status": "abstract_only"}],
    ["wrist data may not reproduce laboratory thresholds"],
    {"free_parameters": ["window_seconds"], "quality_gates": ["signal quality >= 0.9"]},
    {"criterion_measure": "video annotations", "metrics": ["MAE", "F1"]},
)
```

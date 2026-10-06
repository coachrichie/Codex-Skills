# Hockey IQ Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, validate, publish, and install two coordinated Codex skills that analyze five-player hockey support decisions from video and turn findings into representative practices, backed by a traceable public-data corpus and calibrated scoring-probability outputs.

**Architecture:** The work is a staged suite of four independently reviewable subsystems: shared tactical contracts and corpus, probability models, video analysis, and practice design. Portable skill folders own their runtime instructions and scripts; canonical JSON contracts live with the video skill and are copied into the practice skill with a parity test. Network and modeling work are update-time concerns; ordinary analysis must work locally and return `insufficient evidence` when data or calibration is inadequate.

**Tech Stack:** Python 3.11+, pytest, JSON/JSONL, Markdown/YAML, standard-library runtime, ffmpeg/ffprobe command-line tools for authorized media, and an optional modeling environment using pandas and scikit-learn.

**Spec:** `docs/designs/hockey-iq-skills-design.md`

## Global Constraints

- Analyze advanced and elite players and competitive juniors, with support-player movement prioritized over puck-carrier critique.
- Cover zone entries, turnovers, and forecheck recoveries first; analyze all five attacking skaters and relevant defenders.
- Keep observed evidence, derived geometry, tactical inference, system assumptions, research support, and coaching heuristics distinct.
- Never bypass authentication, DRM, paywalls, or platform restrictions; do not commit copyrighted video or restricted datasets.
- Preserve source definitions, licenses, versions, provenance, and review status; public availability does not imply redistribution permission.
- Keep goal probability (`xG`) distinct from high-danger creation probability (`HDCP`); counterfactual estimates are experimental until independently calibrated.
- Return `insufficient evidence` instead of unsupported percentages or invented player, puck, or rink coordinates.
- Complete and validate `hockey-iq-video-analysis` before authoring `hockey-iq-practice-design`.
- Run each new skill's baseline scenarios before writing its `SKILL.md`.

## Review Focus

- Broadcast footage hides a weak-side player: analysis must lower confidence and avoid inventing the five-player shape; exercised in Task 7.
- A successful play follows a structurally poor read: analysis must separate outcome from decision quality; exercised in Task 8.
- A source changes field definitions or license terms: update must quarantine the new version until review; exercised in Task 3.
- A clip lies outside model coverage: probability output must be `insufficient evidence`, not extrapolated precision; exercised in Task 5.
- Practice constraints accidentally prescribe a route instead of preserving a decision: practice validation must reject the plan; exercised in Task 10.

---

## Phase A — Shared Contracts and Living Corpus

### Task 1: Baseline Video-Analysis Evaluations

**Files:**
- Create: `skills/hockey-iq-video-analysis/evals/scenarios.json`
- Create: `skills/hockey-iq-video-analysis/evals/baseline-results.md`
- Create: `skills/hockey-iq-video-analysis/tests/test_eval_fixtures.py`

**Interfaces:**
- Consumes: the approved design specification.
- Produces: `load_scenarios(path: Path) -> list[dict]` fixture contract and documented no-skill failure modes used by Tasks 7–8.

- [ ] **Step 1: Write the failing fixture test**

Assert that seven named scenarios exist: clear controlled entry, valuable unreceived support route, forecheck recovery, risky defense activation, broadcast occlusion, misleading success, and productive failure. Require expected assertions for five-player accounting, support-first reasoning, alternatives, displacement, transition risk, outcome-bias resistance, and uncertainty.

- [ ] **Step 2: Run the test and verify failure**

Run: `python -m pytest skills/hockey-iq-video-analysis/tests/test_eval_fixtures.py -v`  
Expected: FAIL because the scenario file does not exist.

- [ ] **Step 3: Run each scenario without the skill**

Use fresh-context agents, store the exact prompts and concise observed failures in `baseline-results.md`, and do not create `SKILL.md` yet.

- [ ] **Step 4: Add the minimal scenario loader and fixtures**

Define `load_scenarios(path: Path) -> list[dict]` inside the test module. Store only synthetic descriptions or licensed fixture metadata—no third-party video.

- [ ] **Step 5: Verify and commit**

Run the Task 1 test; expect PASS. Commit: `test: establish hockey IQ video baselines`.

### Task 2: Tactical Finding Contract

**Files:**
- Create: `skills/hockey-iq-video-analysis/references/tactical-finding.schema.json`
- Create: `skills/hockey-iq-video-analysis/references/team-profile.schema.json`
- Create: `skills/hockey-iq-video-analysis/scripts/contracts.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_contracts.py`

**Interfaces:**
- Produces: `validate_tactical_finding(record: dict) -> list[str]`, `validate_team_profile(record: dict) -> list[str]`, `load_json(path: Path) -> dict`, and schema version `1.0.0`.
- Contract keys: `source`, `decision_window`, `game_context`, `visibility`, `attackers`, `defenders`, `space_map`, `options`, `recommendation`, `probabilities`, `coaching_priority`, `practice_handoff`, and `provenance`.

- [ ] **Step 1: Write failing contract tests**

Test one complete valid record and invalid records for missing five-player entries, unknown evidence class, missing time horizon, unlabeled counterfactual probability, and unsupported exact coordinates. Test system-neutral defaults plus team profiles for entry, forecheck, offensive-zone rotation, defense activation, transition structure, terminology, and risk tolerance.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest skills/hockey-iq-video-analysis/tests/test_contracts.py -v`  
Expected: FAIL because `contracts.py` and the schema are absent.

- [ ] **Step 3: Implement the contract**

Implement `validate_tactical_finding(record: dict) -> list[str]` using the standard library. Errors are stable machine-readable strings; validation never mutates input.

- [ ] **Step 4: Verify GREEN and commit**

Run Task 2 tests; expect PASS. Commit: `feat: define hockey IQ tactical finding contract`.

### Task 3: Source Registry and Governance

**Files:**
- Create: `skills/hockey-iq-video-analysis/data/sources.jsonl`
- Create: `skills/hockey-iq-video-analysis/data/searches.jsonl`
- Create: `skills/hockey-iq-video-analysis/references/source-policy.md`
- Create: `skills/hockey-iq-video-analysis/scripts/source_registry.py`
- Create: `skills/hockey-iq-video-analysis/scripts/update_sources.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_source_registry.py`

**Interfaces:**
- Produces: `validate_source(record: dict) -> list[str]`, `dedupe_sources(records: list[dict]) -> list[dict]`, `review_state(previous: dict | None, current: dict) -> str`, and `record_discovery_run(query: dict, results: list[dict], failures: list[dict]) -> dict`.
- Source statuses: `candidate`, `reviewed`, `quarantined`, `unavailable`; evidence classes: `structured_data`, `scientific`, `coaching`, `video_exemplar`.

- [ ] **Step 1: Write failing governance tests**

Require stable identifier, URL, authorship/publisher, access date, version/checksum when available, license status, source definition, review status, limitations, and redistribution permission. Test changed license/schema becomes `quarantined`, mirrors deduplicate, inaccessible sources remain in history, and every PubMed/Crossref/OpenAlex or repository discovery run records its query, failures, and incomplete status.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest skills/hockey-iq-video-analysis/tests/test_source_registry.py -v`.

- [ ] **Step 3: Implement registry logic and reviewed seed records**

Seed only sources whose public metadata and reuse terms have been checked. Register Big Data Cup editions individually; do not copy datasets into Git.

- [ ] **Step 4: Verify GREEN and commit**

Run Task 3 tests; expect PASS. Commit: `feat: add governed hockey data source registry`.

### Task 4: Data Adapters, Exemplars, and Retrieval

**Files:**
- Create: `skills/hockey-iq-video-analysis/data/exemplars.jsonl`
- Create: `skills/hockey-iq-video-analysis/scripts/normalize_big_data_cup.py`
- Create: `skills/hockey-iq-video-analysis/scripts/exemplars.py`
- Create: `skills/hockey-iq-video-analysis/scripts/retrieve_examples.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_normalization.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_exemplars.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_retrieval.py`

**Interfaces:**
- Produces: `normalize_event(row: dict, source_id: str) -> dict`, `validate_exemplar(record: dict) -> list[str]`, and `rank_examples(query: dict, records: list[dict], limit: int = 5) -> list[dict]`.

- [ ] **Step 1: Write failing adapter and retrieval tests**

Pin preservation of original event labels, coordinate orientation, source IDs, and raw-to-normalized mappings. Require productive-failure and misleading-success exemplars. Retrieval ranks possession phase, shape, pressure, support roles, scoring mechanism, and transition risk, and reports comparison differences.

- [ ] **Step 2: Verify RED**

Run the three Task 4 test files; expect import failures.

- [ ] **Step 3: Implement minimal normalization, exemplar validation, and deterministic ranking**

The adapter consumes user-downloaded CSV rows and emits JSONL-ready records. Retrieval uses transparent weighted categorical similarity; every result returns `similarities` and `differences`.

- [ ] **Step 4: Verify GREEN and commit**

Run Task 4 tests; expect PASS. Commit: `feat: normalize and retrieve hockey play exemplars`.

## Phase B — Calibrated Probability Layer

### Task 5: Probability Contracts and Runtime Scoring

**Files:**
- Create: `skills/hockey-iq-video-analysis/references/scoring-probabilities.md`
- Create: `skills/hockey-iq-video-analysis/data/models/model-card.json`
- Create: `skills/hockey-iq-video-analysis/scripts/probability.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_probability.py`

**Interfaces:**
- Produces: `score_shot(features: dict, model: dict) -> dict`, `score_continuation(features: dict, model: dict) -> dict`, and `coverage_check(features: dict, model: dict) -> list[str]`.
- Result fields: `metric`, `estimate`, `interval`, `horizon_seconds`, `model_version`, `population`, `comparable_count`, `calibration_status`, `evidence_class`, and `warnings`.

- [ ] **Step 1: Write failing probability tests**

Test xG and HDCP remain separate, probability bounds are `[0, 1]`, intervals contain estimates, counterfactual outputs are labeled experimental, missing coverage returns `estimate: null` with `insufficient evidence`, and unknown features do not silently default.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest skills/hockey-iq-video-analysis/tests/test_probability.py -v`.

- [ ] **Step 3: Implement model-agnostic runtime scoring**

Use JSON model artifacts and standard-library math. The initial committed model card is `unvalidated`; it cannot emit percentages until Task 6 installs a calibrated artifact.

- [ ] **Step 4: Verify GREEN and commit**

Run Task 5 tests; expect PASS. Commit: `feat: add safe probability scoring contract`.

### Task 6: Training, Calibration, and Model Admission

**Files:**
- Create: `skills/hockey-iq-video-analysis/modeling/requirements.txt`
- Create: `skills/hockey-iq-video-analysis/modeling/build_dataset.py`
- Create: `skills/hockey-iq-video-analysis/modeling/train_models.py`
- Create: `skills/hockey-iq-video-analysis/modeling/evaluate_models.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_model_admission.py`

**Interfaces:**
- Produces: `build_examples(events: list[dict]) -> tuple[list[dict], list[int]]`, `train_xg(rows, labels, seed: int) -> dict`, `train_hdcp(rows, labels, seed: int) -> dict`, and `admit_model(report: dict) -> list[str]`.

- [ ] **Step 1: Write failing admission tests**

Require data license/provenance, documented feature definitions, train/temporal-holdout separation, Brier score, log loss, calibration by band, sample counts by tactical context, deterministic seed, and rejection when independent validation or minimum support is absent.

- [ ] **Step 2: Verify RED**

Run Task 6 tests; expect import failures.

- [ ] **Step 3: Implement reproducible modeling scripts**

Use pandas/scikit-learn only in `modeling/`. Export human-readable JSON coefficients, coverage bounds, calibration bands, metrics, and dataset fingerprints. Do not commit downloaded raw data or binary model files.

- [ ] **Step 4: Train candidate models and enforce admission**

Run against reviewed, license-compatible public datasets. If admission fails, keep runtime behavior at `insufficient evidence` and publish the failed calibration report; do not weaken thresholds to force percentages.

- [ ] **Step 5: Verify and commit**

Run Task 5–6 tests. Commit: `feat: add reproducible hockey probability modeling`.

## Phase C — Hockey IQ Video Analysis Skill

### Task 7: Media Evidence and Structured Report Pipeline

**Files:**
- Create: `skills/hockey-iq-video-analysis/scripts/media_probe.py`
- Create: `skills/hockey-iq-video-analysis/scripts/acquire_media.py`
- Create: `skills/hockey-iq-video-analysis/scripts/candidate_segments.py`
- Create: `skills/hockey-iq-video-analysis/scripts/video_overlay.py`
- Create: `skills/hockey-iq-video-analysis/scripts/render_analysis.py`
- Create: `skills/hockey-iq-video-analysis/references/media-workflow.md`
- Create: `skills/hockey-iq-video-analysis/references/tactical-analysis.md`
- Create: `skills/hockey-iq-video-analysis/tests/test_media_probe.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_acquire_media.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_candidate_segments.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_video_overlay.py`
- Create: `skills/hockey-iq-video-analysis/tests/test_render_analysis.py`

**Interfaces:**
- Produces: `acquire_media(source: str, output_dir: Path, authorized: bool) -> dict`, `probe_media(path: Path) -> dict`, `build_sampling_plan(metadata: dict, start: float, end: float) -> dict`, `suggest_segments(timeline: list[dict], focus: set[str]) -> list[dict]`, `build_overlay_script(record: dict) -> str`, `render_overlay(input_path: Path, script: str, output_path: Path) -> dict`, and `render_analysis(record: dict) -> str`.

- [ ] **Step 1: Write failing pipeline tests**

Use generated metadata and synthetic-video fixtures, not copyrighted video. Test refusal without `authorized=True`, unsupported or protected URLs, argument-array subprocess calls, invalid paths, missing ffprobe, discontinuous timestamps, weak-side occlusion, stable temporary player labels, event-based candidate suggestions for entry/turnover/forecheck, required coach confirmation, evidence-class display, ranked options, compact xG/HDCP overlay ranges, and `insufficient evidence` rendering.

- [ ] **Step 2: Verify RED**

Run Task 7 tests; expect import failures.

- [ ] **Step 3: Implement probing, sampling plans, and report rendering**

Commands must be argument arrays without shell interpolation. `acquire_media` supports local paths, direct media URLs, and public URLs handled by an installed `yt-dlp`, but rejects absent authorization and never supplies cookies, credentials, DRM workarounds, or paywall bypasses. Candidate detection proposes timestamps only; deep analysis requires coach confirmation. Overlay rendering uses ffmpeg subtitle/ASS instructions and preserves the source file.

- [ ] **Step 4: Verify GREEN and commit**

Run Task 7 tests; expect PASS. Commit: `feat: add hockey video evidence pipeline`.

### Task 8: Skill Instructions and Forward Evaluation

**Files:**
- Create: `skills/hockey-iq-video-analysis/SKILL.md`
- Create: `skills/hockey-iq-video-analysis/README.md`
- Create: `skills/hockey-iq-video-analysis/agents/openai.yaml`
- Create: `skills/hockey-iq-video-analysis/references/evidence-policy.md`
- Create: `skills/hockey-iq-video-analysis/evals/with-skill-results.md`
- Create: `skills/hockey-iq-video-analysis/tests/test_skill_structure.py`

**Interfaces:**
- Consumes: Tasks 1–7.
- Produces: an automatically discoverable, portable `hockey-iq-video-analysis` skill.

- [ ] **Step 1: Write the failing structure test**

Require valid frontmatter, `description: Use when`, no scaffold placeholders, discoverable references/scripts, explicit authorization boundaries, and support-first output order.

- [ ] **Step 2: Verify RED**

Run Task 8 structure test; expect missing `SKILL.md`.

- [ ] **Step 3: Write the minimal skill against baseline failures**

Keep routing and invariants in `SKILL.md`; move media, evidence, tactical, corpus, and probability detail to the named references.

- [ ] **Step 4: Run the seven original scenarios with the skill**

Record outputs and grade the same assertions used in Task 1. Fix only observed gaps, rerun affected cases, and retain the before/after evidence.

- [ ] **Step 5: Validate and commit**

Run `quick_validate.py`, all video-skill tests, and the seven evaluation cases. Commit: `feat: add validated hockey IQ video analysis skill`.

## Phase D — Practice Design and Integration

### Task 9: Baseline Practice-Design Evaluations

**Files:**
- Create: `skills/hockey-iq-practice-design/evals/scenarios.json`
- Create: `skills/hockey-iq-practice-design/evals/baseline-results.md`
- Create: `skills/hockey-iq-practice-design/tests/test_eval_fixtures.py`

**Interfaces:**
- Produces: five baseline cases covering zone-entry support, turnover attack, forecheck recovery, defense activation/rotation, and regression for limited players or ice.

- [ ] **Step 1: Write failing fixture tests and run them**

Require cues, decisions, defender objectives, transition consequence, success measures, progression, regression, and next-video transfer check.

- [ ] **Step 2: Run no-skill baselines**

Document where generic coaching outputs become choreographed, omit perceptual cues, or ignore transition risk.

- [ ] **Step 3: Verify fixtures and commit**

Commit: `test: establish hockey IQ practice baselines`.

### Task 10: Practice Contract, Renderer, and Skill

**Files:**
- Create: `skills/hockey-iq-practice-design/references/tactical-finding.schema.json`
- Create: `skills/hockey-iq-practice-design/references/practice-plan.schema.json`
- Create: `skills/hockey-iq-practice-design/references/practice-design.md`
- Create: `skills/hockey-iq-practice-design/scripts/validate_input.py`
- Create: `skills/hockey-iq-practice-design/scripts/render_practice_plan.py`
- Create: `skills/hockey-iq-practice-design/SKILL.md`
- Create: `skills/hockey-iq-practice-design/README.md`
- Create: `skills/hockey-iq-practice-design/agents/openai.yaml`
- Create: `skills/hockey-iq-practice-design/tests/test_practice_design.py`
- Create: `skills/hockey-iq-practice-design/tests/test_skill_structure.py`

**Interfaces:**
- Produces: `validate_handoff(record: dict) -> list[str]`, `validate_practice_plan(plan: dict) -> list[str]`, and `render_practice_plan(plan: dict) -> str`.

- [ ] **Step 1: Write failing contract and structure tests**

Reject missing perception/decision targets, absent defender objectives, no transition consequence, no observable measure, no transfer check, or constraints that prescribe the answer. Assert copied tactical schema is byte-identical to Task 2 canonical schema.

- [ ] **Step 2: Verify RED**

Run practice-skill tests; expect missing files.

- [ ] **Step 3: Implement validators, renderer, references, and minimal skill**

The practice output specifies setup, roles, constraints, scoring, questions, workload guidance, success measures, progressions, regressions, and transfer check.

- [ ] **Step 4: Run with-skill evaluations**

Repeat Task 9 scenarios, record results, and correct only demonstrated failures.

- [ ] **Step 5: Validate and commit**

Run `quick_validate.py` and all practice-skill tests. Commit: `feat: add validated hockey IQ practice design skill`.

### Task 11: Cross-Skill Integration

**Files:**
- Create: `tests/test_hockey_iq_integration.py`
- Create: `skills/hockey-iq-video-analysis/tests/fixtures/zone_entry_finding.json`
- Modify: `skills/hockey-iq-practice-design/tests/test_practice_design.py`

**Interfaces:**
- Consumes: the Task 2 finding and Task 10 practice contract.
- Produces: an end-to-end fixture proving decision context survives the handoff.

- [ ] **Step 1: Write the failing integration test**

Assert preservation of decision timestamp, all five support roles, defensive constraints, scoring mechanism, xG/HDCP provenance, uncertainty, transition exposure, coaching priority, and validation measure.

- [ ] **Step 2: Verify RED, implement the minimum bridge, and verify GREEN**

No new orchestration framework: use the JSON handoff already defined. Run the integration test and both skill suites.

- [ ] **Step 3: Commit**

Commit: `test: verify hockey IQ video to practice handoff`.

### Task 12: Repository Verification, Documentation, and Installation

**Files:**
- Modify: `tools/verify_repository.py`
- Modify: `tests/test_repository_layout.py`
- Modify: `tests/test_skills.py`
- Modify: `tests/test_documentation.py`
- Modify: `README.md`
- Modify: `docs/installation.md`
- Modify: `docs/testing.md`

**Interfaces:**
- Produces: repository-wide validation and installation instructions for both skills.

- [ ] **Step 1: Write failing repository tests**

Require both skill directories, validators, test suites, corpus validation, model-admission status, integration fixture, and documentation links. Preserve publication-safety checks and forbidden-file rules.

- [ ] **Step 2: Verify RED and update repository tooling**

Extend `run_skill_checks(root: Path) -> dict` without hard-coding fragile total test counts; report each suite separately.

- [ ] **Step 3: Update public documentation**

Change status from design-only only after all preceding gates pass. Document optional ffmpeg and modeling dependencies separately from standard runtime use.

- [ ] **Step 4: Run the complete verification matrix**

Run: `python -m pytest -q`  
Run: `python tools/verify_repository.py --root .`  
Run both `quick_validate.py` commands.  
Expected: all pass; no sensitive paths, generated caches, downloaded video, raw restricted data, or binary model artifacts are tracked.

- [ ] **Step 5: Install and smoke-test**

Copy the two validated skill directories to the user's Codex skills directory, preserving any existing folders via a recoverable backup. In a new Codex turn, verify both skills are discovered and run one synthetic smoke request per skill.

- [ ] **Step 6: Commit and prepare release review**

Commit: `feat: publish hockey IQ skill suite`. Open a pull request with corpus coverage, model status, evaluation results, known limitations, and installation verification.

## Execution Gates

1. Phase A may merge when contracts, registry, adapters, and retrieval tests pass.
2. Phase B may merge even if candidate models fail admission, provided runtime output remains `insufficient evidence` and the failed calibration report is published.
3. Phase C must pass no-skill versus with-skill evaluation before Phase D begins.
4. Phase D must preserve the shared contract and pass repository publication-safety checks before installation.
5. README status changes from “implementation pending” only after Task 12 completes.


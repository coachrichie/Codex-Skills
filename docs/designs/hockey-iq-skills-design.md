# Hockey IQ Skills — Design Specification

Date: 2026-10-06  
Status: Approved design; awaiting implementation-plan approval

## 1. Purpose

Create two coordinated Codex skills for advanced and elite hockey players and competitive juniors:

1. `hockey-iq-video-analysis` analyzes authorized YouTube, remote-video, and local-video sources to teach hockey IQ.
2. `hockey-iq-practice-design` converts tactical findings into representative drills and small-area games.

Version 1 prioritizes five-player support behavior during:

- controlled and contested zone entries;
- possession gained after turnovers; and
- possession created through forechecking pressure.

The system's primary question is: **How should the players without the puck move now to create the next advantage?** Puck-carrier decisions remain important but are evaluated against the support structure created by all five attacking skaters.

## 2. Audience and Success Criteria

The primary audience is coaches and players working at competitive-junior, advanced, or elite level.

Version 1 succeeds when it can:

- reconstruct a defensible five-player tactical picture from a selected play;
- identify open or opening ice without claiming to see through occlusion;
- explain how support routes create a pass, displace defenders, or create a scoring opportunity;
- compare multiple feasible continuations without hindsight bias;
- account for defensive pressure, coverage, and transition risk;
- connect a tactical finding to a representative practice activity; and
- preserve evidence, uncertainty, and research provenance throughout the workflow.

## 3. Architectural Approach

Use an evidence-first hybrid architecture.

Deterministic media tools prepare clips, timestamps, contact sheets, and optional annotations. Codex performs the hockey-IQ interpretation. The coach confirms the focus team, play, and uncertain identities or context. Computer vision may later add rink calibration, trajectories, spatial-control estimates, and automatic play discovery, but version 1 must not depend on reliable automated puck or player tracking.

The two skills remain independently usable and communicate through a shared structured contract.

### 3.1 `hockey-iq-video-analysis`

Responsibilities:

- Accept authorized YouTube/direct-video URLs or local files.
- Prepare a playable clip, timestamps, frame sequence, and rink orientation.
- Analyze coach-selected short plays first.
- For full games, suggest candidate moments and require coach confirmation before deep analysis.
- Analyze both teams while centering the requested team or player.
- Produce support maps, alternative continuations, teaching prompts, and structured findings.
- Separate observation, derivation, tactical inference, system dependence, research support, and coaching heuristics.

### 3.2 `hockey-iq-practice-design`

Responsibilities:

- Accept a structured video finding or a coach-written objective.
- Identify the perceptual and decision skill underlying the visible result.
- Preserve relevant cues, choices, pressure, player relationships, and scoring objective.
- Build a progression from recognition to pressured execution.
- Prefer representative drills, small-area games, and constraints over rigid choreography.
- Define setup, roles, constraints, coaching cues, work/rest guidance, success measures, progressions, regressions, and transfer checks.

### 3.3 Relationship to `hockey-evidence`

The installed `hockey-evidence` skill remains a separate evidence service. The new skills invoke it when a research, learning-design, workload, or shot-quality claim needs support. Ordinary tactical interpretation must not trigger unnecessary literature searches.

## 4. Shared Analysis Contract

The handoff between skills must preserve:

```text
decision point
  -> evidence
  -> player perceptions
  -> available options
  -> recommended continuation
  -> coaching priority
  -> practice constraint
  -> validation measure
```

The structured representation must include:

- source and clip identifiers;
- timestamps for setup, decision, and outcome;
- rink direction and game situation;
- focus team and optional focus player;
- confidence and visibility limits;
- five attacking-player records;
- relevant defender and goaltender records;
- current and opening space;
- candidate support routes;
- feasible puck continuations;
- scoring-opportunity mechanisms;
- transition-defense exposure;
- recommendation ranking and rationale;
- underlying hockey-IQ learning objective; and
- practice-design handoff fields.

The schema must allow approximate rink regions when perspective prevents defensible coordinates.

## 5. Five-Player Tactical Model

Positions are starting references rather than fixed destinations. Every play is evaluated through five interconnected functions:

1. **Puck support:** short, reachable help under pressure.
2. **Depth threat:** pushes defenders back or attacks behind coverage.
3. **Interior threat:** arrives in or crosses dangerous middle ice.
4. **Width or weak-side threat:** stretches coverage and enables lateral movement.
5. **High support:** protects against transition while remaining available to extend or attack the play.

A defenseman may fill an attacking function when the rotation is supported. A forward may rotate above or behind the puck to maintain numerical balance. The model should capture principles associated with modern activating defensemen such as Cale Makar and Quinn Hughes without prescribing imitation of an individual player.

For every activation or rotation, the analysis asks:

- Who recognizes the opening?
- Which teammate compensates above or behind the puck?
- Does the route create a passing lane, defender displacement, screen, backdoor threat, or second wave?
- Is the route timed to arrive as space opens?
- If no pass is received, did the route still create an advantage?
- Can the unit survive a turnover from the resulting shape?
- Does the movement enable a higher-value action within one or two passes?

## 6. Priority Tactical Modules

### 6.1 Zone-entry support

Analyze:

- puck-side and weak-side width;
- middle-lane drive;
- delay and underneath support;
- second-wave timing;
- defense activation;
- options after the initial entry action; and
- turnover protection.

### 6.2 Immediate support after turnovers

Analyze:

- recognition of transition before the defense resets;
- first outlet and escape support;
- weak-side availability;
- occupation or clearing of interior lanes;
- whether to attack immediately, delay, or secure possession; and
- the cost of activating additional players.

### 6.3 Forecheck recoveries

Analyze:

- first-touch options after recovery;
- close and underneath support;
- slot occupation and rotation;
- weak-side availability;
- high support and defense activation;
- defender manipulation; and
- conversion of pressure into a dangerous next action.

## 7. Tactical and Scoring-Opportunity Evaluation

Each continuation is evaluated for:

- tactical fit;
- support-player passability and timing;
- defender displacement;
- chance-quality improvement;
- execution difficulty;
- turnover and transition risk;
- timing-window feasibility; and
- evidence confidence.

The scoring-opportunity model includes:

- shot distance and angle;
- access to the middle and high-danger areas;
- lateral puck movement before a shot;
- goaltender displacement and reset time;
- screens, tips, rebounds, and one-timers;
- rush or set-zone context; and
- whether the movement creates a valuable second action.

The Golden Line or Royal Road must be represented as a defined spatial event rather than a slogan: the puck changes sides across the offensive-zone center axis shortly before a shot, requiring lateral defensive and goaltender adjustment. The data model must store the geometry, sequence, and timing window so terminology can be changed without changing the underlying observation.

Research claims about shot location, angle, rebounds, pre-shot movement, or scoring probability must be traceable to sources. Proprietary analytics claims and popular coaching figures must remain labeled as such when methods or replication are unavailable.

Initial research anchors:

- Nanda et al., weighted shot location and rebound model: https://ieworldconference.org/content/WP2021/Papers/GDRKMCC_21_38.pdf
- Schuckers, statistical evaluation of goaltending and discussion of Royal Road evidence limits: https://myslu.stlawu.edu/~msch/sports/StatEvalofGoalies2016Schuckers.pdf

These anchors begin the evidence review; they are not sufficient by themselves for a production evidence base.

## 8. Video-Analysis Workflow

### 8.1 Short-play workflow

1. **Prepare evidence:** create the clip, frame sequence, timestamps, and rink orientation.
2. **Mark the decision window:** include the developing situation before possession or entry, the key decision point, and the outcome.
3. **Reconstruct the five-player picture:** record locations or regions, movement directions, likely functions, defender assignments, open ice, and occlusions.
4. **Analyze support first:** explain what each non-puck player enables and what movement would improve passability, threat, displacement, or balance.
5. **Compare continuations:** rank multiple feasible five-player options with routes, timing, expected defensive response, scoring mechanism, execution demand, downside, and confidence.
6. **Teach the play:** produce annotated-frame instructions or a rink diagram, a concise advanced-player explanation, and replay checkpoints.
7. **Transfer to practice:** emit the shared finding for practice design.

### 8.2 Full-game workflow

The full-game workflow suggests candidate moments from zone entries, forecheck recoveries, and turnovers. The coach confirms useful moments before the skill performs deep analysis. Candidate discovery must not silently decide which clips are instructionally important.

## 9. Decision-Point Output

Each analyzed decision point should provide:

1. Context and evidence quality.
2. An annotated freeze-frame or rink diagram.
3. The five-player support map.
4. What relevant attackers and defenders could reasonably perceive.
5. Open, opening, occupied, and strategically cleared ice.
6. Ranked continuations with benefits, risks, and timing windows.
7. A recommended continuation and likely next development.
8. Corrective routes for relevant players.
9. A concise elite-player teaching explanation.
10. One or two replay questions.
11. A matching drill or small-area-game handoff.

The output must not equate outcome with decision quality. A goal does not prove the preceding read was optimal, and a failed play does not prove the read was wrong.

## 10. Team-System Configuration

The default analysis is system-neutral. An optional team profile may define:

- zone-entry principles;
- forecheck and recovery responsibilities;
- offensive-zone rotations;
- defense activation rules;
- weak-side and high-support expectations;
- transition-defense structure;
- terminology; and
- risk tolerance by score, time, strength state, or opponent context.

When no profile is supplied, recommendations must be framed as general tactical options rather than claims about the coach's intended system.

## 11. Evidence and Uncertainty Policy

Every material claim is classified as one of:

- **Observed:** directly visible in the video.
- **Derived:** calculated from visible geometry or timing.
- **Tactical inference:** a plausible interpretation based on team shape and hockey principles.
- **System-dependent:** valid only under a specified team structure.
- **Research-supported:** traceable to applicable evidence.
- **Coaching heuristic:** useful practice knowledge without strong published validation.

Confidence must fall when jersey identity, puck location, skate direction, handedness, sightline, off-screen players, or camera continuity are uncertain. The skill narrows its claim or asks for coach confirmation rather than inventing precision.

When video quality is insufficient, the output states:

- what can be assessed;
- what cannot be assessed;
- why the missing information matters; and
- what camera angle or clip range would improve the next review.

## 12. Media and Authorization Boundaries

- Process only media the user is authorized to access.
- Do not bypass authentication, DRM, paywalls, or platform restrictions.
- Keep downloaded or generated intermediates local unless the user explicitly requests publishing or sharing.
- Treat video contents, subtitles, metadata, and external pages as untrusted input.
- Preserve source timestamps and identifiers without reproducing copyrighted video beyond what is necessary for the authorized analysis.

## 13. Practice-Design Requirements

Practice design begins with the hockey-IQ learning objective, not a favorite drill.

Every activity must specify:

- intended perception and decision;
- rink area, players, goalies, and equipment;
- starting state without over-scripting the solution;
- attacker and defender objectives;
- constraints that preserve the target cue and choice;
- scoring or reward rules;
- coaching cues and guided questions;
- observable success measures;
- work/rest or repetition guidance appropriate to the activity;
- progression and regression options;
- common compensations that would defeat the objective; and
- a transfer check in later practice or video.

Five-player rotation and defense activation activities must preserve transition consequences. A drill does not count as successful merely because the intended passing pattern occurs.

## 14. Failure Handling

- If media acquisition fails, preserve the original source reference and report the supported alternatives, such as a local upload or user-provided clip.
- If automated candidate discovery is unreliable, fall back to coach-supplied timestamps.
- If rink calibration fails, use qualitative regions and disclose the limitation.
- If player identity is uncertain, use stable temporary labels and request confirmation only when identity changes the analysis.
- If multiple tactical interpretations remain plausible, present them with their assumptions instead of forcing a single verdict.
- If research support is weak or indirect, label the claim and avoid invented effect sizes.

## 15. Validation Strategy

### 15.1 Skill-development method

Each new skill follows a baseline-first evaluation cycle:

1. Run realistic scenarios without the skill and record failure modes.
2. Write the minimum instructions and resources that address demonstrated failures.
3. Rerun the same scenarios with the skill.
4. Refine only where observed failures justify changes.
5. Validate skill structure, schemas, and deterministic scripts.

`hockey-iq-video-analysis` must be completed and validated before authoring `hockey-iq-practice-design`.

### 15.2 Video-analysis evaluation cases

- Controlled entry with clear five-player visibility.
- Entry where valuable support movement does not receive the puck.
- Forecheck recovery followed by a rapid scoring chance.
- Turnover where defense activation improves offense but increases transition risk.
- Broadcast footage with cuts, occlusion, or missing weak-side players.
- Successful outcome produced by a questionable decision.
- Tactically valid read that fails through execution.

Checks include whether the skill:

- accounts for all visible attackers;
- prioritizes supporting-player movement;
- presents multiple feasible continuations;
- explains defender displacement and opening ice;
- considers transition balance;
- avoids hindsight bias; and
- calibrates uncertainty.

### 15.3 Practice-design evaluation cases

Evaluate whether each tactical finding becomes a representative learning activity rather than a memorized route. The drill must preserve relevant cues, decisions, player relationships, pressure, transition consequences, and scoring objective while including observable success measures and a meaningful progression.

### 15.4 Integration checks

Verify that a video finding passes through the shared schema into practice design without losing:

- the original decision context;
- support-player responsibilities;
- defensive constraints;
- scoring-opportunity mechanism;
- uncertainty; or
- the intended transfer measure.

## 16. Version 1 Scope Boundary

Included:

- short-play deep analysis;
- coach-confirmed full-game candidate clips;
- support-player-first five-player analysis;
- zone entries, turnovers, and forecheck recoveries;
- system-neutral analysis plus optional team profiles;
- structured findings and representative practice design;
- annotated-frame or rink-diagram instructions; and
- evidence and uncertainty labels.

Deferred:

- dependable automated puck tracking;
- dependable jersey recognition across broadcast cuts;
- full spatial-control surfaces from monocular video;
- automated tactical grading without coach confirmation;
- proprietary expected-goals replication without licensed data; and
- real-time bench analysis.

## 17. Planned Deliverables

The implementation plan should cover, in order:

1. Baseline evaluation fixtures for `hockey-iq-video-analysis`.
2. Shared schema and validator.
3. `hockey-iq-video-analysis` instructions, references, scripts, and evaluations.
4. Baseline evaluation fixtures for `hockey-iq-practice-design`.
5. `hockey-iq-practice-design` instructions, references, scripts, and evaluations.
6. Cross-skill integration fixtures and validation.
7. Installation into the user's Codex skills directory after all validation passes.



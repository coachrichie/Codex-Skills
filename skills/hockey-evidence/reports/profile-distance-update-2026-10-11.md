# Profile-distance evidence update — 2026-10-11

## Sources and review scopes

This imports a targeted source audit, not a new exhaustive PubMed/Crossref/OpenAlex update.
Six genuine works were retained; erroneous attributions and unsupported equations were excluded.
Primary publisher, PubMed/PMC, author-manuscript and institutional sources support the paraphrases.
OpenAlex served discovery only. Links are in the study provenance and
[profile-distance reference](../references/profile-distance.md); no full text is redistributed.

| Study ID | Review status and audited scope |
| --- | --- |
| `hockey-budarick-2020` | `abstract_only`: abstract reviewed, manuscript excerpts available, complete full-text review incomplete. 2020 print / online 2018 are one work. |
| `bandy-pojskic-2025` | `abstract_only`: refereed conference abstract reviewed, not journal article. Institutional URN is canonical; RG DOI is unverified locator only. |
| `bandy-vanden-tillaar-2025` | `abstract_only`: relevant full-text sections reviewed via indexed publisher rendering; full-paper review incomplete. |
| `inline-speed-wu-2025` | `abstract_only`: accessible full text, relevant abstract/methods/evidence tables reviewed; partial-review scope preserved conservatively. Secondary scoping review. |
| `hockey-allisse-2023` | Upgraded to `full_text_reviewed` for relevant full-text sections/table only; secondary systematic review by Bournival et al. Historical ID and seed provenance retained. |
| `hockey-skating-khandan-2022` | Upgraded to `full_text_reviewed` for relevant full text; original criterion-comparison study using skate/shank/pelvis IMUs. |

## Queries, counts and deduplication

Re-check exact titles/DOIs in `data/searches.jsonl`, then combine each title with leg length,
BMI, height, mass, participants and results. Follow recorded primary-source URLs and
preserve access failures. The source audit did not retain exact search strings or complete
result universes; these strategies reproduce targeted checks, not an exhaustive search replay.

Before: 5 studies. Reviewed candidates: 6, including 2 existing records. Added: 4.
Upgraded: 2. After: 9 valid records. No new duplicates; 2018/2020 Budarick deduplicated by DOI.
Both topic-index filename variants are rebuilt from the same corpus deterministically.
Existing distance keywords retrieve all four added works; no keyword expansion is required.

## Failures and coverage limits

Budarick DOI fetch returned 403; PubMed initially 429, indexed abstract remained readable.
McGill direct manuscript retrieval failed. MDPI direct pages returned repeated 429;
indexed journal sections exposed relevant bandy methods/results/limitations. DiVA conference
PDF extraction initially exposed only the cover and screenshots timed out; institutional
author record supplied the abstract and URN. DiVA bandy journal PDF retrieval timed out.
Nature succeeded via trailing slash after initial failure. PMC later returned CAPTCHA;
Frontiers and Nature supplied relevant primary text. RG DOI registration was not independently
verified. Missing fields are not inferred. The log remains `complete: false`.

The bounded search found no validated hockey height/weight equation for metres per detected
wrist push. This is not a systematic absence claim. Bandy and inline speed skating are indirect
to hockey; conference and partial-review scopes remain explicit. Do not propagate the bandy
journal's swapped male height/mass table entries or inconsistent glide-time sex result.

## Product implications and next gaps

Keep fixed 125/225 cm (first four burst / later rhythm pushes) as ordinary release default.
Standing height as a leg-length proxy supports only an application prior, with the specified
shrinkage/clamp/rounding; weight/BMI is not a distance multiplier. Pelvis `2 ± 6%` does not
validate Garmin wrist accuracy. Distinguish step, glide, same-skate stride, sensor trajectory
and application push distance.

The reference defines held-out player-grouped activation criteria separately for ice, inline
and combined data. No improved-accuracy claim precedes passing them. Current layers are
GPS-independent scientific baseline and local personal known-distance calibration.
Scope adjustment: global model/training, server upload and GPS are explicitly out of scope
for the current beta and this update. Any future work requires a separate design/consent/
validation decision; it is not a current architecture layer or requirement. Add no uploads,
automatic calibration, GPS dependency or runtime surface selector; app display/time behavior
is untouched. Next gaps are wrist-event criterion validation, representative turning/hockey
sequences, direct inline-hockey data, and complete review of inaccessible candidate sections.

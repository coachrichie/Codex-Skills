# Initial Hockey Evidence Update

Date: 2026-09-28  
Corpus version: initial-seed-2026-09-28

## Queries

The seed query was the named-source list in `docs/superpowers/specs/2026-09-15-shiftsense-hockey-design.md`, covering hockey physiology, hockey testing, wearable skating, commercial wearable validity, and energy-expenditure validity.

## Sources

Metadata was checked against Europe PMC/PubMed records and the linked publisher or PubMed Central landing pages. Five records were retained: two direct ice-hockey reviews, one direct ice-hockey wearable validation study, and two indirect general-wearable validation reviews.

## Counts

- Candidates reviewed: 5
- Retained studies: 5
- Deduplicated: 0
- `abstract_only`: 5
- `full_text_reviewed`: 0
- `bibliographic_only`: 0

All seed records are restricted records. They are either abstract-only or, when no abstract has been reviewed, **nur bibliografisch erfasst**; neither status is equivalent to a full-text review.

## Failures

No source request failure was recorded for the metadata checks. Full-text extraction was intentionally not performed in this seed; therefore this is not a full systematic-review update.

## Deduplication

DOI, PMID, and PMCID were cross-checked where available. No duplicate identifiers were found. Study IDs are stable local IDs and do not replace source identifiers.

## Coverage limits

This seed is limited to the five sources already named in the ShiftSense specification. It does not claim exhaustive coverage of ice hockey, inline hockey, long-track speed skating, or other gliding sports. No findings are represented as `full_text_reviewed`. Indirect evidence is explicitly labeled and must not be promoted to direct hockey evidence by topic matching.

## Next gaps

- Expand reproducible searches across PubMed, Crossref, and OpenAlex for inline hockey and long-track speed skating.
- Review accessible full texts and record findings, methods, uncertainty, and limitations with line-level provenance.
- Add hockey-specific HR/recovery, shift duration, load, and Garmin wrist-sensor validation studies.
- Validate any proposed distance, energy, impact, or recovery algorithm against criterion measurements before product claims.

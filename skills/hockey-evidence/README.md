# Hockey Evidence

A Codex skill for citation-first ice-hockey research, ShiftSense/Garmin app audits, and traceable wearable-data algorithm design.

## Modes

- **Update:** query PubMed, Crossref, and OpenAlex and log search coverage.
- **Literature review:** summarize structured records with provenance and review status.
- **App audit:** classify claims as supported, indirectly supported, or insufficiently supported.
- **Algorithm design:** separate literature findings, transfer assumptions, app-specific choices, free parameters, and validation plans.

The evidence hierarchy prioritizes ice hockey, then inline hockey and long-track speed skating, followed by justified evidence from other gliding or intermittent sports.

## Scientific boundaries

The corpus is versioned and source-linked but **not exhaustive**. It does not guarantee coverage of every published or indexed study. This skill is **not medical** advice, is not a medical device, and must not be used for diagnosis.

Records with `abstract_only` or `bibliographic_only` status are not equivalent to full-text-reviewed evidence. Do not promote them silently. Copyright remains with the original publishers and authors; the repository does not include copyrighted scientific full texts.

Algorithm proposals remain experimental until tested against representative criterion measurements. Wrist-worn Garmin data must not be treated as interchangeable with sensors at other body locations without validation.

## Structure and testing

- `data/`: study records, searches, and topic indexes
- `references/`: research, assessment, audit, and algorithm rules
- `scripts/`: deterministic update and analysis helpers
- `tests/`: fixture-based regression and acceptance tests

Run:

```text
python -m pytest tests -q
python scripts/validate_corpus.py --input data/studies.jsonl
```

See the repository [installation guide](../../docs/installation.md) and [testing guide](../../docs/testing.md).

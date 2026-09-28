# Garmin Connect IQ

A Codex skill for developing, debugging, and answering API questions about Garmin Connect IQ applications, Monkey C, and the Toybox API.

## Use cases

- check Toybox methods, types, permissions, API levels, deprecations, and device availability;
- implement or debug Connect IQ apps, data fields, widgets, and watch faces;
- review manifests and compatibility assumptions;
- search an optional private local API mirror when the owning Toybox module is unknown.

The entrypoint is `SKILL.md`. Garmin's API documentation is not redistributed by this repository. `scripts/sync-api-docs.ps1` can create a private local mirror under `references/api-docs` for development use, subject to Garmin's current agreement.

## Third-party rights

Garmin, Connect IQ, Toybox, and related marks belong to Garmin or their respective owners. Garmin's API pages and other Program Materials remain subject to Garmin's terms and rights and are intentionally excluded from this repository. The repository's MIT License applies only to self-authored material where the contributor has the right to license it.

## Updating and validation

From this skill directory:

```powershell
powershell -File scripts/sync-api-docs.ps1
```

Before refreshing, review Garmin's current Connect IQ Developer Agreement. After refreshing, keep the generated mirror untracked, check local links, and run the Codex skill validator. See the repository [installation guide](../../docs/installation.md) and [testing guide](../../docs/testing.md).

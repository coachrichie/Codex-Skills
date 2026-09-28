# Codex Skills

Reusable Codex skills for Garmin Connect IQ development and evidence-based hockey analytics.

## Included skills

| Skill | Purpose |
|---|---|
| [Hockey Evidence](skills/hockey-evidence/README.md) | Research ice-hockey science, audit ShiftSense/Garmin claims, and design traceable wearable-data algorithms. |
| [Garmin Connect IQ](skills/garmin-connect-iq/README.md) | Develop and debug Monkey C applications using a searchable Toybox API reference. |

## Quick start

Clone the repository, then copy the skill you need into your Codex skills directory:

```text
git clone https://github.com/coachrichie/Codex-Skills.git
```

Codex normally discovers personal skills under `$CODEX_HOME/skills`, or under `~/.codex/skills` when `CODEX_HOME` is unset. Back up an existing skill folder before replacing it. See the [installation guide](docs/installation.md) for Windows, macOS, and Linux commands.

Example requests:

- “Use the Hockey Evidence skill to audit this recovery metric.”
- “Use the Garmin Connect IQ skill to check whether this Toybox API is available on my target devices.”

## Quality and scope

The Hockey Evidence corpus is versioned and source-linked, but it is not guaranteed to contain every published study. It is not medical advice and must not be used for diagnosis. Algorithm proposals remain experimental until validated against appropriate criterion measurements.

Garmin API documentation is not redistributed in this repository. Garmin owns its documentation and trademarks; see the [Garmin skill notes](skills/garmin-connect-iq/README.md).

## Project documentation

- [Installation](docs/installation.md)
- [Testing](docs/testing.md)
- [Publishing](docs/publishing.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

Self-authored repository content is available under the [MIT License](LICENSE). Third-party content remains subject to its original rights and terms.

# Codex Skills

Reusable Codex skills for Garmin Connect IQ development and evidence-based hockey analytics.

## Included skills

| Skill | Purpose | Status |
|---|---|---|
| [Hockey Evidence](skills/hockey-evidence/README.md) | Research ice-hockey science, audit ShiftSense/Garmin claims, and design traceable wearable-data algorithms. | Available |
| [Garmin Connect IQ](skills/garmin-connect-iq/README.md) | Develop and debug Monkey C applications using a searchable Toybox API reference. | Available |
| [Hockey IQ Video Analysis + Practice Design](docs/designs/hockey-iq-skills-design.md) | Analyze five-player support behavior in video and turn tactical findings into representative practice activities. | Approved design; implementation pending |

## In development: support-player-first Hockey IQ

The next two coordinated skills focus on advanced and elite players and competitive juniors:

- `hockey-iq-video-analysis` will analyze authorized YouTube and local-video plays, beginning with zone entries, turnovers, and forecheck recoveries.
- `hockey-iq-practice-design` will convert those findings into representative drills and small-area games.

The design treats all five skaters as a connected offensive unit. Its central question is how players without the puck should move to become passing options, displace defenders, attack opening ice, create high-danger opportunities, and preserve transition balance. It also covers modern defense activation, shot angle and distance, pre-shot lateral movement, and Golden Line/Royal Road concepts with explicit evidence and uncertainty labels.

Its evidence layer is a federated, versioned corpus of open play and tracking datasets, scientific research, attributed coaching knowledge, and authorized public-video exemplars. Sources retain license, provenance, definitions, limitations, and update history; public availability is not treated as permission to redistribute copyrighted material.

Video outputs will distinguish shot goal probability (xG) from the probability that a proposed continuation creates a high-danger chance. Estimates will include uncertainty, model provenance, data coverage, and calibration status; unsupported situations return `insufficient evidence` rather than false precision.

Read the complete [Hockey IQ skills design specification](docs/designs/hockey-iq-skills-design.md).

> The Hockey IQ skills are currently a reviewed design proposal, not installable skills. Implementation and validation are the next stage.

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
- [Hockey IQ skills design](docs/designs/hockey-iq-skills-design.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

Self-authored repository content is available under the [MIT License](LICENSE). Third-party content remains subject to its original rights and terms.

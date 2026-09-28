# Publishing

## Release checklist

1. Update skill source files and documentation through reviewed commits.
2. Run all commands in [testing.md](testing.md).
3. Run `python tools/verify_repository.py --root .`.
4. Inspect `git status --short`, `git diff --check`, and `git ls-files`.
5. Confirm no tokens, personal activity files, copyrighted papers, caches, or local user paths are tracked.
6. Push the verified `main` commit.
7. Confirm the remote commit, README, repository visibility, and skill folders.

Hockey literature updates must retain query logs, provenance, review status, and incomplete-run markers. Garmin API-mirror updates should originate from the official Connect IQ API documentation and preserve upstream notices.

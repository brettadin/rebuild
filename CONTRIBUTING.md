# Contributing

Please read `Rebuild.md` and `Rebuild_Architecture.md` before contributing.

Contributing workflow

1. Pick one feature at a time from `Rebuild.md`.
2. Create a new feature branch from `main` (or `dev`) named `feature/<short-description>`.
3. Implement the feature and add tests (unit + integration as needed).
4. Update `docs/logs/dev_log.md` and `docs/logs/patch_log.md` describing the change.
5. File a PR and request review: do not merge until tests pass and documentation is updated.

Notes about local data

- Use `data/local/` for locally uploaded datasets or large files that you do not want tracked in git. These files should be documented in `docs/references/`.
- Keep test fixtures small, real, and under `data/sample/` so they remain version-controlled and reproducible.

Developer expectations

- All sample data must come from a real source and be documented in `docs/references/`.
- Tests should use the `tests/fixtures` directory and reference live-cited sources.
- Keep changes focused: one change per PR, where practicable.
# Patch Log

This patch log contains a minimal record of changes:

- 2025-12-11 — Initial repo scaffolding and README created. See `README.md` for starting instructions.
- 2025-12-11 — Added `data/local/` for local uploaded files; this folder is gitignored to prevent committing large local datasets. Also added `.gitignore` entries and `data/local/README.md` with guidelines.
- 2025-12-11 — Phase 0 implemented: minimal desktop app shell using PySide6, initial launcher, logging adapter, config, and a smoke/unit test. Added `run_app.py`, `scripts/run_app.ps1`, `scripts/run_tests.ps1`, and `requirements.txt`.
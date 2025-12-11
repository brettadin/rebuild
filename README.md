# Rebuild (Spectroscopy Desktop App)

Welcome! This repository contains the specification and architecture for a local desktop application focused on spectroscopy data import, search, and graphing.

Key specification files (source-of-truth):

- `Rebuild.md` — App Rebuild Specification (features, data sources, rules, testing, etc.)
- `Rebuild_Architecture.md` — Proposed repository structure and folder mapping, meant for implementers and agents
- `WorkOrder.md` — Ordered roadmap for implementation; follow this roadmap feature-by-feature

Purpose of this README

- Point new developers and automated agents to the two specification files above, which should be consulted before beginning work.
- Outline the repository scaffold and initial next steps for contributors and coding agents.

Quick links (local):
- Rebuild spec: `Rebuild.md`
- Architecture: `Rebuild_Architecture.md`

Minimal repo structure (already created):
- `src/` — Application source (UI, graphing, search, data_access, domain, projects, notes, config, platform)
- `data/` — Real sample/cached data and fixtures
- `docs/` — Human-facing documentation and developer logs
- `tests/` — Unit & integration tests
- `scripts/` — Helper scripts (fetching sample data, build, tests)
- `assets/` — Icons & UI assets
- `config/` — Config files & provider endpoints

Initial steps for contributors and agents

1. Read both `Rebuild.md` and `Rebuild_Architecture.md` to understand the functional and architectural requirements.
2. The architecture file maps features to folders; start implementing a single feature at a time (per the spec).
3. Add real sample data to `data/sample/` from the approved sources (NIST, HITRAN, MAST, PDS, ESO). Cite each file with a reference in `docs/references/`.
4. For the first coding tasks, choose a narrow-scope feature (e.g., F1 local CSV import) and implement a feature branch. Create tests and documentation for each completed feature.

Important: Local user files

- `data/local/` is intended to store user-uploaded or locally acquired datasets. This folder is gitignored by default to prevent large datasets or sensitive files from being accidentally committed.
- If you need sample data that _is_ tracked for tests or examples, put it under `data/sample/` and document its provenance in `docs/references/`.

Conventions & important notes

- All sample/fixture data MUST be real and have provenance (URL/DOI) and be referenced in `docs/references/`.
- Follow the "feature-by-feature" workflow from `Rebuild.md`.
- Tests and docs are required for each feature; add them as part of the PR.

Next steps (for the agent):
- Implement an initial skeleton for `src/data_access/local` importer plus a test fixture in `data/sample/` and a simple unit/integration test in `tests/`.

If you're an automated agent: begin by choosing one small, well-scoped feature from the spec and create a PR for review.

---

This README intentionally keeps instructions short — read the spec for the concrete requirements.


Phase 0: run & test the minimal app locally


1. Install dependencies (create a virtual environment for dev):

   PowerShell (Windows):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the app:

   - Windows PowerShell: `scripts\run_app.ps1` or `python run_app.py` in the activated venv.

3. Run tests:

   - Windows PowerShell: `scripts\run_tests.ps1` or `python -m pytest -q` in the activated venv.


# First Steps for New Contributors / Agents

This is a short checklist you can follow to get started quickly.

1. Read `Rebuild.md` and `Rebuild_Architecture.md` in the repo root.
2. Choose your first feature (recommendation: F1 Local Importer for CSV/TXT).
3. Create a branch named `feature/importer-csv`.
4. Implement a simple importer under `src/data_access/providers/local/` that can parse a CSV and produce a `dataset` model.
   - Keep importers pluggable and metadata-aware (units, source, phase where available).
5. Add a small sample file (real dataset) in `data/sample/` and create a corresponding reference file in `docs/references/`.
6. Write unit tests in `tests/unit/` that validate the importer and dataset model (unit conversion, metadata parsing).
7. Write integration tests in `tests/integration/` that run an import → graph pipeline (mock the UI/graphing where necessary).
8. Update `docs/logs/dev_log.md` and `docs/logs/patch_log.md` with a summary and change records.

When done, open a PR following the `CONTRIBUTING.md` conventions and add test coverage.
# Patch Log

This patch log contains a minimal record of changes:

- 2025-12-11 — Initial repo scaffolding and README created. See `README.md` for starting instructions.
- 2025-12-11 — Added `data/local/` for local uploaded files; this folder is gitignored to prevent committing large local datasets. Also added `.gitignore` entries and `data/local/README.md` with guidelines.
- 2025-12-11 — Phase 0 implemented: minimal desktop app shell using PySide6, initial launcher, logging adapter, config, and a smoke/unit test. Added `run_app.py`, `scripts/run_app.ps1`, `scripts/run_tests.ps1`, and `requirements.txt`.
- 2025-12-11 — Phase 1 started/completed (Local import/export): added `DatasetModel` and `DatasetRepo`, `LocalFileImporter` with CSV/TXT parsing and CSV export, sample data under `data/sample/local_lab/sample_spectrum.csv`, unit/integration tests for import/export, and docs reference `docs/references/local_lab_sample_spectrum.md`.
- 2025-12-11 — Phase 2 implemented: graphing core (GraphManager, DatasetViewModel, ColorManager) and Matplotlib integration; added `GraphPanel` UI panel, sample_spectrum2.csv, and integration test for importing and plotting two datasets. Added matplotlib requirement.
- 2025-12-11 — Phase 3 implemented: dataset metadata helpers and inference (`src/domain/datasets/dataset_metadata.py`), metadata fields extended (`DatasetMetadata`), importer attaches inferred metadata, GraphPanel shows dataset metadata on selection, and unit + UI tests added.
- 2025-12-11 — Phase 4 implemented: favorites model and repo with JSON persistence, `FavoritesPanel` UI with segmented tabs, GraphPanel integration ("Add to Favorites"), and unit/integration tests for favorites behavior.
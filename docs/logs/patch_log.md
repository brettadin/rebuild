# Patch Log

Concise summary of repo and development patches. Duplicates were removed and entries normalized.

## 2025-12-11

- Initial repo scaffolding, README, `data/local/`, `.gitignore` entries.
- Phase 0: App shell implemented (PySide6), launcher, logging adapter, config, and smoke/unit test.
- Phase 1: Local import/export (CSV/TXT), dataset model and importer.
- Phase 2: Graphing core and `GraphPanel` UI (Matplotlib, GraphManager).
- Phase 3–5: Dataset metadata, favorites, and project/session support.
- Phase 6: Notes & Annotations — `NoteModel`, `NoteRepo`, `NotesPanel`, graph overlays, and tests.
- Phase 7: NIST line search + overlays (client, parser, UI), hover tooltips, UX polish.
- Phase 8: PDS/Solar System search — `PdsClient`/`pds_parser`, PlanetModel/Repo, `PlanetSearcher`, `SolarSystemSearchPanel`, fixture and integration test.
- Phase 9 (start): Standard Archive Searches — added fixture-mode `HitranClient`, `hitran_parser`, `MoleculeSearcher`, `MoleculeSearchPanel` UI, and sample CO2 fixture; integration tests added.

Notes:
- If log duplication resumes, check for scripts or automation that append to logs; prefer manual commit of log updates or scripted deduplication checks.# Patch Log

This patch log is a concise record of changes:

- 2025-12-11 — Repo scaffolding (README, initial structure).
- 2025-12-11 — Phase 0: App shell implemented (PySide6), launcher, logging.
- 2025-12-11 — Phase 1: Local import/export (CSV/TXT) and dataset model.
- 2025-12-11 — Phase 2: Graphing core and GraphPanel UI.
- 2025-12-11 — Phase 3–5: Metadata, Favorites, and Projects implemented.
- 2025-12-11 — Phase 6: Notes & Annotations—models, UI, overlays.
- 2025-12-11 — Phase 7: NIST line search + overlays, tooltips, and UX polish.
- 2025-12-11 — Phase 8: PDS Solar System search — `PdsClient`, parser, `PlanetSearcher`, `PlanetModel`, UI (`SolarSystemSearchPanel`), sample PDS fixture and integration test.

This patch log contains a minimal record of changes:

- 2025-12-11 — Initial repo scaffolding and README created.
- 2025-12-11 — Added `data/local/`, `.gitignore`, and `data/local/README.md`.
- 2025-12-11 — Phase 0: app shell, launcher, logging, tests.
- 2025-12-11 — Phase 1: Local import & export (CSV/TXT), dataset model.
- 2025-12-11 — Phase 2: Graphing core and `GraphPanel` UI.
- 2025-12-11 — Phase 3 & 4: Dataset metadata and favorites.
- 2025-12-11 — Phase 5: Projects & sessions (save/restore snapshots).
- 2025-12-11 — Phase 6: Notes & Annotations (NoteModel, NoteRepo, UI, overlays).
- 2025-12-11 — Phase 7: NIST line search/provider, overlay manager, tooltips, UI/UX improvements.
- 2025-12-11 — Phase 8: Solar System (PDS) search, PlanetModel/Repo, SolarSystemSearchPanel, sample fixture, and integration test.

This patch log contains a minimal, unique record of changes:

- 2025-12-11 — Phase 7: NIST line search/provider, overlay manager, tooltips, UX polish.
- 2025-12-11 — Phase 8: Solar System (PDS) search including `PdsClient`, `pds_parser`, `PlanetSearcher`, `PlanetModel`, `PlanetRepo`, `SolarSystemSearchPanel`, sample fixture, and integration test.

- 2025-12-11 — Added `data/local/`, `.gitignore` updates, and `data/local/README.md`.
- 2025-12-11 — Phase 0 completed (app shell, launcher, logging, basic tests).
- 2025-12-11 — Phase 1 completed (local import/export): CSV/TXT importer and exporter, dataset model.
- 2025-12-11 — Phase 2 completed (graphing): GraphManager, DatasetViewModel, color management, GraphPanel.
- 2025-12-11 — Phase 3 & 4 completed (metadata & favorites): dataset metadata handling and favorites repo/UI.
- 2025-12-11 — Phase 5 completed (projects/sessions): Project model, repo, UI, and snapshots.
- 2025-12-11 — Phase 6 implemented: notes and annotations and overlay UI; tests added.
- 2025-12-11 — Phase 7 implemented: NIST line search and overlays, hover tooltips, inline editing, overlay toggles.
- 2025-12-11 — Phase 8 implemented: PDS solar system search, planet model, search panel, and load-to-graph pipeline; sample PDS fixture and tests added.

- 2025-12-11 — Initial repo scaffolding and README created. See `README.md` for starting instructions.
- 2025-12-11 — Added `data/local/` for local uploaded files; this folder is gitignored to prevent committing large local datasets. Also added `.gitignore` entries and `data/local/README.md` with guidelines.
- 2025-12-11 — Phase 0 implemented: minimal desktop app shell using PySide6, initial launcher, logging adapter, config, and a smoke/unit test. Added `run_app.py`, `scripts/run_app.ps1`, `scripts/run_tests.ps1`, and `requirements.txt`.
- 2025-12-11 — Phase 1 started/completed (Local import/export): added `DatasetModel` and `DatasetRepo`, `LocalFileImporter` with CSV/TXT parsing and CSV export, sample data under `data/sample/local_lab/sample_spectrum.csv`, unit/integration tests for import/export, and docs reference `docs/references/local_lab_sample_spectrum.md`.
- 2025-12-11 — Phase 2 implemented: graphing core (GraphManager, DatasetViewModel, ColorManager) and Matplotlib integration; added `GraphPanel` UI panel, sample_spectrum2.csv, and integration test for importing and plotting two datasets. Added matplotlib requirement.
- 2025-12-11 — Phase 3 implemented: dataset metadata helpers and inference (`src/domain/datasets/dataset_metadata.py`), metadata fields extended (`DatasetMetadata`), importer attaches inferred metadata, GraphPanel shows dataset metadata on selection, and unit + UI tests added.
- 2025-12-11 — Phase 4 implemented: favorites model and repo with JSON persistence, `FavoritesPanel` UI with segmented tabs, GraphPanel integration ("Add to Favorites"), and unit/integration tests for favorites behavior.
- 2025-12-11 — Phase 5 implemented: projects model, repo & UI, Save As, last project persistence, favorites merge/replace behavior, project snapshots for datasets/favorites/graph_config, and related tests & docs.
- 2025-12-11 — Phase 6 started: added `NoteModel`, `NoteRepo`, `NotesPanel`, annotation overlay in graphs, and integration with Project snapshots; tests for notes & annotations added.
- 2025-12-11 — Phase 7 implemented: NIST line search provider, parser, UI panel, and `LineOverlayManager`, enabling overlay of NIST lines on graphs. Added sample NIST fixture, parser & client, integration tests, and docs.
- 2025-12-11 — Added interactive & UX features: click-to-create notes on the graph, hover tooltips for line overlays, and more robust NIST client parameters and headers. Updated tests to cover new behaviors and docs to describe UX changes.
- 2025-12-11 — Phase 7 continued: added note snapping to nearest datapoint, inline note editing in the `NotesPanel`, overlay visibility toggling, and refactored to avoid UI freezing by scheduling modal dialogs on the Qt event loop. Updated tests for new UX and fixed flaky tests.


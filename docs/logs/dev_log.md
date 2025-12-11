# Dev Log

This development log records important milestones, decisions, and design notes. Entries are kept concise and in chronological order.

## 2025-12-11

- Repo scaffolding and initial setup (app skeleton, launcher, logging adapter, config defaults).
- Added `data/local/`, updated `.gitignore`, and added initial README and sample data guidance.
- Phases 1–5 completed: local import/export, graphing core, dataset metadata, favorites, and project/session support.
- Phase 6: Implemented Notes & Annotations — `NoteModel`, `NoteRepo`, `NotesPanel`, annotation markers on graphs, snap-to-nearest, persistence tests.
- Phase 7: Implemented NIST line search and overlays — `NistClient`, `nist_parser`, `LineSearcher`, `LineOverlayManager`, NIST UI; added UX improvements (click-to-create notes with non-blocking dialog scheduling, overlay tooltips, inline note edits, per-dataset overlay toggle).
- Phase 8: Implemented PDS/Solar System search (fixture mode) — `PdsClient`, `pds_parser`, Planet model/repo, `PlanetSearcher`, `SolarSystemSearchPanel`, sample PDS fixture (Jupiter), and integration test for plotting planetary spectra.

### Notes & Action Items

- Fixed duplicate entries across dev and patch logs; consolidated and normalized content.
- For CI and automated test runs, consider setting `REBUILD_DISABLE_AUTO_POPUPS=true` to suppress interactive dialogs (e.g., QInputDialog/QMessageBox).
- If any scripts append to docs/logs, make sure they append unique entries to avoid duplicates.

- Phase 6: Implemented Notes & Annotations — `NoteModel`, `NoteRepo`, `NotesPanel`, annotation markers on graphs, and persistence tests.
- Phase 7: Implemented NIST line search and overlays — `NistClient`, `nist_parser`, `LineSearcher`, `LineOverlayManager`, NIST UI; added UX improvements (click-to-create notes with non-blocking dialog scheduling, overlay tooltips, snap-to-nearest, inline note edits, per-dataset overlay toggle).
- Phase 8: Implemented a fixture-first PDS client and parser (`PdsClient`, `pds_parser`), Planet model/repo, `PlanetSearcher`, `SolarSystemSearchPanel`, sample PDS fixtures and an integration test to load/plotted planetary spectra.

- For CI and automated test runs, consider setting `REBUILD_DISABLE_AUTO_POPUPS=true` to suppress interactive dialogs (e.g., QInputDialog/QMessageBox) when tests run in non-interactive environments.
- If there are scripts that append to logs, make sure they perform deduplication or append only unique entries.

This development log summarizes notable implementation milestones and design decisions. Duplicate entries were removed and records normalized.

- 2025-12-11: Repository created and initial scaffolding put in place (work order, data/local readme, .gitignore updates).
- 2025-12-11: Phase 0 completed — PySide6 app shell with launcher, logging adapter, config defaults and a smoke/unit test that validates app import/launch.
- 2025-12-11: Phase 1–5: Implemented local import/export, graphing core, dataset metadata, favorites, and project/session save/load behavior (see per-phase docs for details).
- 2025-12-11: Phase 6: Notes & Annotations implemented — `NoteModel`, `NoteRepo`, `NotesPanel`, and annotation overlays with snap-to-nearest logic and persistence; tests added.
- 2025-12-11: Phase 7: NIST line search and overlays — `NistClient`, `nist_parser`, `LineSearcher`, `LineOverlayManager`, and search UI implemented. Extended UX: click-to-create notes, non-blocking dialogs via `QTimer.singleShot`, overlay tooltips, snapping, inline editing, and overlay visibility toggles.
- 2025-12-11: Phase 8: PDS/Solar System search — added `PdsClient` fixture loader, `pds_parser`, planets domain/repo/searcher, `SolarSystemSearchPanel`, sample PDS fixture (Jupiter), and end-to-end integration test; GraphPanel supports plotting planetary spectra.

Notes and action items:
- Log duplication was observed and corrected. If the log files are updated programmatically by scripts, ensure the script appends unique entries only; otherwise prefer manual commit of log changes.
- For automated CI/test workflows, consider setting `REBUILD_DISABLE_AUTO_POPUPS=true` to suppress interactive dialogs.

This is the project 'dev log' — record decisions, notes, system constraints, and other design details during implementation. Each change should append a short entry with a date, the change summary, and the relevant context or PR link.

- 2025-12-11: Created `data/local/` for locally uploaded files and updated `.gitignore` to ignore data and cache folders; included `data/local/README.md` for usage guidance. Added `WorkOrder.md` link to top-level README and docs/index.
- 2025-12-11: Implemented Phase 0 (Foundation & Skeleton): added a minimal PySide6 app shell (`MainWindow`), launcher (`src/platform/launcher.py`), logging adapter, configuration (`src/config/defaults.yaml`), and unit test (`tests/unit/test_app_launch.py`). Created run scripts and test harness; updated README and logs.
- 2025-12-11: Phase 6 implementation started: added notes feature with `NoteModel`, `NoteRepo`, `NotesPanel` UI and `AnnotationManager` overlay for graph markers. Integrated notes into project snapshots and added unit + integration tests to validate note persistence and graph overlay.
- 2025-12-11: Phase 7 implementation started: NIST ASD line search & overlay support via `NistClient`, `nist_parser`, `LineSearcher`, `NistSearchPanel`, `LineOverlayManager`, and sample fixtures for testing. Added tests & docs for search and overlays.
- 2025-12-11: Added interactive features and improvements: click-to-create notes directly on the canvas, hover tooltips for NIST line overlays, and more robust NIST client HTTP configuration (User-Agent, retries). Updated tests and docs accordingly.
- 2025-12-11: Continued Phase 7: implemented snapping to nearest datapoint, inline note editing in `NotesPanel`, and overlay visibility toggling. Also refactored click handler to schedule modal dialog display on the Qt event loop to prevent freezing caused by synchronous modal dialogs in Matplotlib callbacks.


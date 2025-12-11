# Dev Log

This is the project 'dev log' — record decisions, notes, system constraints, and other design details during implementation. Each change should append a short entry with a date, the change summary, and the relevant context or PR link.

- 2025-12-11: Created `data/local/` for locally uploaded files and updated `.gitignore` to ignore data and cache folders; included `data/local/README.md` for usage guidance. Added `WorkOrder.md` link to top-level README and docs/index.
- 2025-12-11: Implemented Phase 0 (Foundation & Skeleton): added a minimal PySide6 app shell (`MainWindow`), launcher (`src/platform/launcher.py`), logging adapter, configuration (`src/config/defaults.yaml`), and unit test (`tests/unit/test_app_launch.py`). Created run scripts and test harness; updated README and logs.
 - 2025-12-11: Phase 6 implementation started: added notes feature with `NoteModel`, `NoteRepo`, `NotesPanel` UI and `AnnotationManager` overlay for graph markers. Integrated notes into project snapshots and added unit + integration tests to validate note persistence and graph overlay.
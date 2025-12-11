# Documentation Index

This repository follows the Rebuild specification and architecture for a desktop spectroscopy application. The canonical documents for the project are:

- `Rebuild.md` — App rebuild specification (functional goals, data sources, testing rules). This is the primary feature and process spec.
- `Rebuild_Architecture.md` — Proposed source layout and mapping for feature areas to the repository folders.
- `WorkOrder.md` — Ordered roadmap that describes the phased implementation of features.

Starting points for new contributors and agents

1. Read `Rebuild.md` and `Rebuild_Architecture.md` in the repo root.
2. See `docs/references/` for provider details and data provenance. Any sample fixture must be listed there.
3. Before implementing a feature, create a feature branch and update `docs/logs/patch_log.md` and `docs/logs/dev_log.md`.

Roadmap: Review `WorkOrder.md` before starting work — it contains the ordered phases and "done" criteria for each feature.

Project structure quick glance

- `src/` — application source
- `data/` — real sample and cache
- `docs/` — documentation & logs
- `tests/` — tests (unit & integration)

If you're an agent: Identify the smallest deliverable feature from `Rebuild.md` (e.g., import a CSV and graph it) and implement one feature at a time. Add tests and update docs as you go.
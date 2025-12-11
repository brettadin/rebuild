# Notes & Annotations (Phase 6)

This document describes the new Notes & Annotations feature (Phase 6):

- Notes are represented by `NoteModel` and persisted via `NoteRepo`.
- Notes can be dataset-level (no x position) or point-specific (with `x` coordinate).
- Notes are shown in a new `NotesPanel` UI and a dataset-specific list in `GraphPanel`.
- Notes are rendered as vertical markers on the graph when they have an x position via `AnnotationManager` and `GraphManager`.
- Notes are included in Project snapshots and are restored when a project is opened.

Interactive features:

- Click-to-create: You can left-click on the graph canvas (within the axis area) to add a note at that spectral x position — the app prompts for text and associates the note with the active dataset.
- Notes can be created programmatically via `GraphPanel.add_note_at(x, text, dataset_id)` useful for testing or integration.
- Edit notes inline: `NotesPanel` has an `Edit Note` action that allows editing an existing note's text in-place.
- Snapping: when you click near an existing datapoint, the click snaps to the nearest dataset's datapoint if within a small tolerance (default 0.1 nm) so annotations can align precisely with data points.

Tooling/UX improvements (future):

- Click-and-drag modes, snapping to nearby peaks.
- Inline note editor in `NotesPanel` to edit a note text without deleting/recreating.

Usage:

1. Add or select a dataset in the `GraphPanel`.
2. Click **Add Note** and provide the note text and optionally an x position.
3. Notes appear under the `Notes` panel and as a small vertical marker on the graph.
4. Notes are stored in `data/storage/notes.json` and are included in project save files.

Design details:

- `NoteModel` includes `id`, `text`, `dataset_id`, `x` (float), `created_at` and optional `metadata`.
- `NoteRepo` handles JSON persistence and includes `list_for_dataset` and `list` helpers.
- `AnnotationManager` is a lightweight overlay renderer for Matplotlib axes.
- `GraphManager` includes `set_annotations` to set overlays and refresh the plot.

Testing & Validation:

- Unit tests for `NoteModel` and `NoteRepo` (`tests/unit/`).
- Integration tests for note creation and project snapshot/restore (`tests/integration/test_notes_and_annotations.py`).

Future improvements:

- Add interactive graph selection to create notes at clicked positions.
- Add tooltips and hover behavior for annotations to show note text without opening the `NotesPanel`.
- Support note editing UI.

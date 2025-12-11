# Project Panel

The Project Panel UI allows creating, listing, opening, saving, and deleting projects.

Features:


This is a minimal implementation to support Phase 5. Integration with dataset and favorites state will be implemented next.

Project snapshot behavior:

- When saving a project, the UI captures:
  - The list of dataset IDs currently loaded in the dataset repo.
  - A snapshot of the datasets (x/y arrays and metadata) into the project file.
  - Favorites segmented lists for datasets/elements/molecules/planets/moons/stars.
  - Basic graph configuration (which traces are displayed and whether unit conversion is active).
- When opening a project, the UI restores:
  - Datasets in the project snapshot into the in-memory dataset repo.
  - Project-specific favorites, overwriting the app favorites state.
  - Graph traces based on the saved configuration.

Notes and Limitations:

- The Project Panel is conservative about listing valid project files: it only lists JSON files that contain a `name` key in the top-level JSON. This prevents unrelated JSON files (e.g. favorites) from appearing as projects.
- Project files are stored under `data/templates/projects/` by default; favorites and other storage files should not be placed in the same directory to avoid confusion.

Project UI polish:

- A `Project` menu is available in the main menu with quick actions: `New Project`, `Open Project`, `Save Project`, `Save Project As...`, and `Close Project`.
- `Save As...` lets the user pick a project filename under the configured `projects_dir`.
- There's a `Replace favorites on open` checkbox in the Project Panel. By default, favorites are merged (project favorites are added to existing favorites); if checked, opening a project will replace the app’s favorites with the project's favorites.
- The app stores the last-opened project in `data/storage/last_project.txt` (or as configured) and attempts to open it on startup.
- The project JSON includes a `notes` field (empty list by default). Note saving and restore will be implemented in Phase 6; the app currently stores this as an empty snapshot for future compatibility.

New UI notes:

- The Project Panel adds a `Save As...` option to create a new project file name.
- The Main Window persists the last-opened project in `data/storage/last_project.txt` (or as configured) and attempts to load that project at startup.
- The `Favorites` panel includes a "Project favorites only" checkbox to show project-local favorites (from the last-loaded project) when checked.

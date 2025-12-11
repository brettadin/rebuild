# data/local/

This folder is where users or the application can store local datasets or uploads that should not be tracked in version control.

Guidelines

- Do not commit files in this folder to the repository with sensitive or large data.
- Add metadata and provenance for any datasets here by creating a corresponding reference in `docs/references/` (for example `docs/references/<file>_reference.md`).
- This folder is ignored by git by default; the only file kept in the repo is this `README.md` (so the folder exists in the repo structure).

How to use it

- If you import a local file using the app, consider copying it into `data/local/` to make it persistent across app restarts.
- For testing or CI, keep small fixture files under `data/sample/` (those should be real, documented subsets with references in `docs/references/`).

Policy

- No synthetic data: files placed here for examples or tests must be real and have provenance recorded.

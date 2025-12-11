# NIST Line Search & Overlays (Phase 7)

This feature adds the ability to search NIST ASD and overlay atomic line positions on graphs.

Key features:

- `NistClient` wrapper supports online calls to NIST ASD and can be pointed to a local fixture for testing. The client sets a `User-Agent` and has basic retry/backoff logic; the tool also supports local fixtures for deterministic tests and offline use.
- `nist_parser` maps raw results into `LineResult` models.
- `LineSearcher` is a search provider that calls `NistClient` and returns `LineResult` instances.
- `NistSearchPanel` provides a lightweight UI to search by element, ion and wavelength range and overlay selected lines.
- `LineOverlayManager` draws red vertical markers and labels for line positions in the `GraphPanel`.
- Hover tooltips: when the cursor moves near a line overlay, a tooltip shows element and wavelength (nm) for quick inspection. When energy levels are available, the tooltip shows lower/upper energy values as well.
- Overlay visibility: `GraphPanel` exposes both a global overlay toggle and per-dataset overlay toggles to reduce visual clutter on-demand.

Usage:

- Open the NIST search dock in the main window.
- Enter element (e.g., Fe) and optional ion, range.
- Click Search; select a line and click "Overlay Selected" to add the line marker to the graph.

Testing:

- Unit test `tests/unit/test_nist_parser.py` validates parsing sample fixtures.
- Integration test `tests/integration/test_nist_line_overlay.py` validates overlay rendering from fixture search results.

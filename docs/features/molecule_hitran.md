# Molecule Search (HITRAN-like)

This feature adds a basic Molecule Search functionality that queries a fixture-based HITRAN dataset and returns molecular spectra suitable for plotting.

What this provides:

- A fixture-based `HitranClient` to search sample JSON fixtures in `data/sample/hitran`.
- A `MoleculeSearcher` that wraps the client and returns `MoleculeResult` objects.
- A `MoleculeSearchPanel` UI with a search form and result list; search results can be loaded into the main graph.

Notes:

- The current client is in fixture-first mode for reproducible testing; a live API client can be added later.
- Each search result includes a `spectrum` with `units_x`, `units_y`, `x` and `y` arrays and minimal `metadata`.

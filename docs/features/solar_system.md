# Solar System Search (Phase 8)

This feature adds the ability to search NASA PDS (Geosciences node) for solar system planetary spectra and load them into the graph.

Key features:

- `PdsClient` loads local fixtures (JSON) used for testing and offline demo. Online fetching is left as a future enhancement.
- `pds_parser` converts fixture JSON into `DatasetModel` (x/y arrays and metadata).
- `PlanetSearcher` provides a simple search API for planets and returns `PlanetResult` entries.
- `SolarSystemSearchPanel` provides a UI to search planets (by name) and load the selected spectrum into the graph as a new dataset.

Usage:

- Open the Solar System (PDS) Search panel in the main window.
- Enter a planet name (e.g., "Jupiter") and click Search. Fixture results (if present) will be listed.
- Select one result and click Load Selected to add it to the dataset repo and the graph panel.

Testing:

- Integration test `tests/integration/test_solar_system_search.py` validates searching and loading a sample Jupiter fixture from `data/sample/pds/sample_jupiter_spectrum.json`.

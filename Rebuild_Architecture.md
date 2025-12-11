Below is a proposed repository structure for the rebuild, designed to be:
	• Desktop-UI friendly (any language/toolkit).
	• Clean separation of UI, domain logic, data access, and storage.
	• Aligned with your feature spec (import, graphing, searches, libraries, notes, projects, etc.).
	• Clear enough that an AI coding agent can drop code into the right places.
I’ll start with the top-level layout, then walk through each folder and how it maps to your features.

1. Top-level layout
repo-root/
├── src/                 # All application code (desktop app)
│   ├── ui/
│   ├── graphing/
│   ├── search/
│   ├── data_access/
│   ├── domain/
│   ├── projects/
│   ├── notes/
│   ├── config/
│   └── platform/
├── data/                # Real example data + cache, not code
│   ├── sample/
│   ├── cache/
│   └── templates/
├── docs/                # Human-readable docs
│   ├── spec/
│   ├── user/
│   ├── dev/
│   ├── logs/
│   └── references/
├── tests/               # Automated tests
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/             # Helper scripts for build, test, packaging
├── assets/              # Icons, images, UI assets (non-data)
├── config/              # Top-level configuration files
└── README.md

This avoids using “app/ vs data/” for both code and files, which gets confusing. Instead:
	• src/ = code.
	• data/ = actual data files (sample + cache).
	• docs/ = all written documentation, logs, features, wishlist, etc.

2. src/ – Application code
src/
├── ui/
├── graphing/
├── search/
├── data_access/
├── domain/
├── projects/
├── notes/
├── config/
└── platform/

2.1 src/ui/ – Desktop UI
All view/layout code, independent of where data comes from.
Suggested structure:
src/ui/
├── main_window/         # Main app window + menu
├── panels/
│   ├── search_panel/    # Search form + filters + results
│   ├── graph_panel/     # Main graph view, controls
│   ├── favorites_panel/ # Segmented favorites view
│   ├── notes_panel/     # Notes list + details
│   ├── project_panel/   # Project/session selection
│   └── references_panel/# Database/scholarly references UI
└── components/
    ├── forms/
    ├── dialogs/
    ├── widgets/
    └── icons/

Mapping to your spec:
	• Search form with filters → search_panel/.
	• Single main graph area → graph_panel/.
	• Segmented favorites → favorites_panel/.
	• Projects/sessions → project_panel/.
	• References + hyperlinks → references_panel/.
The desktop toolkit (Qt/.NET/etc.) dictates the file extensions, but the folder purpose stays the same.

2.2 src/graphing/ – Plotting & visuals
src/graphing/
├── core/
│   ├── graph_manager.*       # Orchestrates graphs, datasets, overlays
│   ├── dataset_view_model.*  # Abstraction of plotted data
│   └── color_manager.*       # Ensures distinct colors per dataset
├── axes/
│   ├── units.*               # Wavelength ↔ wavenumber, etc.
│   ├── scales.*              # Linear/log axis management
│   └── labels.*              # Title/axis label logic
├── overlays/
│   ├── line_overlays.*       # NIST/HITRAN line markers
│   ├── band_overlays.*       # Shaded bands, atmospheric windows, etc.
│   └── annotation_markers.*  # Note markers on graphs
└── renderers/
    ├── molecules_renderer.*  # 3D molecular motion visuals
    ├── atoms_renderer.*      # Atomic diagrams/info
    ├── stars_renderer.*      # Object images & info overlays
    ├── planets_renderer.*
    └── moons_renderer.*

	• Unit conversion, native units, axis labels → axes/.
	• Multiple datasets with distinct colors → core/ + color_manager.
	• Notes as markers on graphs → overlays/annotation_markers.
	• Domain-specific visuals (molecules, atoms, stars, planets, moons) → renderers/.

2.3 src/search/ – Search logic (UI-independent)
src/search/
├── models/
│   ├── search_query.*        # Unified query model (object type, range, tags)
│   ├── search_filter.*       # Phase, instrument, etc.
│   └── search_result.*       # Common result representation
├── providers/
│   ├── line_searcher.*       # Element line search logic (uses data_access/nist)
│   ├── molecule_searcher.*   # Molecule IR/UV-Vis (HITRAN, PDS etc.)
│   ├── planet_searcher.*     # Solar system planetary searches
│   ├── star_searcher.*       # Stellar searches (Sun + others)
│   └── moon_searcher.*       # Moon searches
└── presets/
    ├── saved_searches.*      # Saved search definitions
    └── defaults.*            # Built-in default searches

	• Clean search forms feed search_query + search_filter.
	• Providers translate high-level searches into data access calls (see below).
	• Saved searches / presets live in presets/.

2.4 src/data_access/ – External APIs & local files
src/data_access/
├── providers/
│   ├── nist/
│   │   ├── nist_client.*      # Calls NIST ASD APIs / scraping
│   │   └── nist_parser.*      # Converts results to internal models
│   ├── hitran/
│   │   ├── hitran_client.*    # HITRAN/HAPI access
│   │   └── hitran_parser.* 
│   ├── mast/
│   │   ├── mast_client.*      # MAST/Exo.MAST
│   │   └── mast_parser.*
│   ├── pds/
│   │   ├── pds_client.*       # NASA PDS spectral libraries
│   │   └── pds_parser.*
│   ├── eso/
│   │   ├── eso_client.*       # ESO archive
│   │   └── eso_parser.*
│   └── local/
│       ├── local_file_importer.* # CSV/TXT/FITS etc.
│       └── local_metadata.*      # Attach phase, source, etc.
├── cache/
│   ├── cache_manager.*        # Manages on-disk cache (see /data/cache)
│   └── cache_index.*          # Keeps track of what’s cached
└── mappers/
    ├── provider_to_domain.*   # Map provider responses → domain models
    └── units_normalizer.*     # Normalize units & metadata on ingest

Responsibilities:
	• Providers/: talk to external archives and local files. They know nothing about UI.
	• Cache/: handles saving/reusing data in data/cache/.
	• Mappers/: convert external formats into internal, domain-consistent structures.
This is the main enforcement point for:
	• “No synthetic data”
	• Phase tagging
	• Unit normalization
	• Provenance (track source + URLs)

2.5 src/domain/ – Domain models & libraries
src/domain/
├── elements/
│   ├── element_model.*        # Element, ions, basic properties
│   ├── element_repo.*         # Access layer for elements
│   └── transitions_model.*    # Transition states, energies
├── molecules/
│   ├── molecule_model.*       # Names, aliases, structure
│   ├── molecule_repo.*        # Library access
│   └── modes_model.*          # Vibrational/rotational modes
├── stars/
│   ├── star_model.*           # Properties, classification
│   └── star_repo.* 
├── planets/
│   ├── planet_model.*         # Properties (radius, atmosphere, etc.)
│   └── planet_repo.*
├── moons/
│   ├── moon_model.*
│   └── moon_repo.*
├── datasets/
│   ├── dataset_model.*        # Generic dataset wrapper (source, units, phase)
│   ├── dataset_repo.*         # Access to all loaded datasets
│   └── dataset_metadata.*     # Provenance, tags, phase, etc.
└── references/
    ├── reference_entry.*      # One reference (DB or paper)
    ├── reference_repo.*       # Manage references
    └── mappings.*             # Link datasets → references

This layer holds the app’s view of the world:
	• Elements, molecules, stars, planets, moons.
	• Dataset-level metadata (units, phase, source, tags).
	• Reference links.
Everything else (UI, data_access, graphing) should consume these models.

2.6 src/projects/ – Projects / sessions
src/projects/
├── project_model.*            # Represents one project/session
├── project_repo.*             # Create/load/save projects
└── serializers/
    ├── project_serializer.*   # Save to disk (JSON, etc.)
    └── project_migrations.*   # Upgrade project formats if needed

Each project remembers:
	• Loaded datasets and their sources.
	• Favorites in that project context.
	• Notes.
	• Basic graph configuration.
Projects will be saved into something like data/templates/projects/ or a dedicated project folder (see /data below).

2.7 src/notes/ – Notes and annotations
src/notes/
├── note_model.*               # Plain text + formatting metadata
├── note_repo.*                # Save/load notes
├── note_formatter.*           # Markdown-lite formatter, etc.
└── note_links.*
    ├── note_to_dataset.*      # Link notes to datasets
    └── note_to_position.*     # Link notes to specific wavelengths/features

	• Keeps notes separate from UI and graphing.
	• Supports:
		○ Dataset-level notes.
		○ Point-specific notes (wavelength/wavenumber).
	• Formatting (Markdown-style basics) handled in note_formatter.*.

2.8 src/config/ – App config (code side)
src/config/
├── defaults.*                 # Default app settings
├── providers_config.*         # Endpoints, API keys (if any), timeouts
├── graph_defaults.*           # Default axis units, styles, colors
└── paths.*                    # Where cache, logs, projects live on disk

This lets the app control:
	• Provider configuration (NIST, HITRAN, MAST, PDS, ESO).
	• Graph defaults.
	• File locations.

2.9 src/platform/ – OS-specific details
src/platform/
├── fs_adapter.*               # File system adapters (paths, permissions)
├── os_detection.*             # Windows vs macOS behaviors
├── logging_adapter.*          # Logging integration
└── launcher.*                 # Entry point, startup logic

This isolates platform details (Windows vs macOS) so the rest of the app stays clean.

3. data/ – Real data & cache
data/
├── sample/
│   ├── nist/                  # Real, small NIST line samples
│   ├── hitran/                # Real, small HITRAN subsets
│   ├── mast/
│   ├── pds/
│   ├── eso/
│   └── local_lab/             # Your own lab/observational subsets
├── cache/
│   ├── providers/             # Cached responses from each provider
│   └── graphs/                # Optional cached render metadata
└── templates/
    ├── projects/              # Example project files
    └── notes/                 # Example note structures/templates

Rules:
	• No synthetic data: everything in sample/ must be real subsets from actual archives or your own lab, with references stored in docs/references/.
	• cache/ is managed only via the app (through src/data_access/cache).

4. docs/ – Documentation, logs, references
docs/
├── spec/
│   ├── app_spec.md            # This spec
│   ├── feature_roadmap.md
│   └── architecture.md
├── user/
│   ├── getting_started.md
│   ├── user_guide.md
│   └── faq.md
├── dev/
│   ├── coding_guidelines.md
│   ├── data_sources.md        # HITRAN/MAST/NIST/PDS/ESO descriptions
│   ├── provider_notes.md      # Technical notes per provider
│   └── testing_strategy.md
├── logs/
│   ├── patch_log.md
│   ├── dev_log.md
│   ├── features.md
│   └── wishlist.md
└── references/
    ├── databases.md           # Links/docs for HITRAN, MAST, NIST, etc.
    └── scholarly_refs.md      # Papers/articles cited, by dataset or feature

This is where:
	• Your spec lives and evolves.
	• Patch log, dev log, features, wishlist are all kept (nothing dropped).
	• Database and scholarly references are centralized and cross-linked.

5. tests/ – Automated tests
tests/
├── unit/
│   ├── test_units_conversion.*    # Graphing units
│   ├── test_search_models.*       # Search query/filter logic
│   ├── test_domain_models.*       # Elements/molecules/etc.
│   └── ...
├── integration/
│   ├── test_import_and_graph.*    # F1 + F2
│   ├── test_nist_line_overlay.*   # F3
│   ├── test_solar_system_search.* # F4
│   └── test_standard_searches.*   # F5
└── fixtures/
    ├── real_nist_subset.ext       # Actual sample data
    ├── real_hitran_subset.ext
    ├── real_pds_spectrum.ext
    └── ...

All fixtures must come from real data and be documented in docs/references/.

6. scripts/ – Build, test, packaging helpers
scripts/
├── fetch_sample_data.*       # Script to download/update real sample subsets
├── run_tests.*               # Run all tests in /tests
├── build_app.*               # Build binaries/bundles
└── package_installer.*       # Create installers or app bundles for Win/macOS

These scripts are for coding agents / dev automation, not for you to manage manually.

7. assets/ & config/
assets/
├── icons/
├── logos/
└── ui/
    ├── layout_mockups/
    └── style_guides/

config/
├── app_config.yaml           # High-level app config
├── providers.yaml            # API endpoints, toggles for providers
└── logging.yaml              # Logging verbosity/targets

	• assets/ holds non-data visuals (icons, logos, mockups).
	• config/ holds external-facing configuration that can be edited without touching code (e.g., endpoint URLs, timeout settings, whether a provider is enabled).


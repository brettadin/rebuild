Below is an ordered roadmap that:
	• Respects “one feature at a time until functional.”
	• Builds a vertical slice at each step (you can actually use the app after each phase).
	• Prioritizes your v1 requirements: local import/export, graphing, NIST line search, solar system search, standard archive search, plus favorites/notes/projects.
For each step I’ll say:
	• What the feature is.
	• What code areas it touches (in your repo structure).
	• What “DONE” means before moving to the next step.
You do not have to do anything in these steps; this is for your coding agents.

Phase 0 – Foundation & Skeleton (no science features yet)
Goal: A minimal desktop app that launches on Windows/macOS with the repo/file layout in place.
Touches:
	• src/ui/main_window/
	• src/platform/launcher.*
	• src/config/
	• docs/spec/app_spec.md
	• tests/ basic harness
Work:
	1. Create repo structure exactly as designed (src/, data/, docs/, tests/, etc.).
	2. Implement a desktop main window (blank shell) that:
		○ Opens on Windows and macOS.
		○ Has a simple menu or toolbar (even if empty).
	3. Wire logging & basic config:
		○ src/platform/logging_adapter.*
		○ src/config/defaults.*
	4. Set up test runner and run a trivial test (e.g., “app imports successfully”).
DONE when:
	• You can double-click / run the app on Windows and macOS and see a basic window.
	• Tests run and pass (even if they only test something trivial).
	• docs/spec/app_spec.md exists and contains this spec.
	Do not implement any import, graphing, search, or notes yet.

Phase 1 – Feature 1: Local Data Import & Export (F1)
Goal: Load real local datasets (multiple file types) and export them back out. No plots yet.
Touches:
	• src/data_access/providers/local/
	• src/domain/datasets/
	• src/ui/panels/ (a simple file import/export panel)
	• data/sample/local_lab/
	• tests/integration/test_local_import_export.*
Work:
	1. Implement dataset model:
		○ src/domain/datasets/dataset_model.*
		○ Fields: x-values, y-values, units, object type (if known), phase (if known), provenance.
	2. Implement local file importer:
		○ local_file_importer.* with pluggable handlers:
			§ CSV
			§ TXT
			§ One spectral FITS example (if relevant).
		○ Attach metadata (units, guessed type) via local_metadata.*.
	3. Implement export:
		○ At least CSV with:
			§ Data arrays
			§ Units
			§ Basic metadata.
	4. Build a minimal UI to:
		○ Pick a file.
		○ Import it.
		○ Show a textual summary table (e.g., file name, N rows, units).
		○ Export back out to CSV.
	5. Create real sample data in data/sample/local_lab/:
		○ Small snippets from your real lab data (no fakes).
DONE when:
	• You can import at least:
		○ One CSV.
		○ One TXT.
		○ One additional format (e.g., FITS if needed).
	• The dataset appears in an internal list with correct units and metadata.
	• You can export a chosen dataset and re-import it with no structural changes.
	• Integration test: “Import sample dataset → export → re-import → same size & units” passes.

Phase 2 – Feature 2: Core Graphing with Multiple Datasets (F2)
Goal: Plot multiple datasets on one main graph, with correct units and distinct colors.
Touches:
	• src/graphing/core/ (graph_manager, dataset_view_model, color_manager)
	• src/graphing/axes/ (units, scales, labels)
	• src/ui/panels/graph_panel/
	• tests/integration/test_import_and_graph.*
Work:
	1. Implement graph_manager.*:
		○ Accepts one or more dataset_model objects.
		○ Renders them on a single graph.
	2. Implement unit/axis logic:
		○ Use dataset’s native axis by default (wavelength vs wavenumber).
		○ Provide a toggle to convert (where physically meaningful).
		○ Show current units on the axis.
	3. Implement distinct colors:
		○ color_manager.* ensures each dataset on a graph has a unique color.
	4. Update UI:
		○ graph_panel/ shows:
			§ Available datasets (from Phase 1).
			§ One main graph area.
			§ Controls: add/remove dataset from graph; toggle unit conversion.
	5. Add linear axes now; log scaling can be a toggle, but doesn’t need deep polish yet.
DONE when:
	• You can import 2–3 different local files and see them overlaid on one graph.
	• Each dataset has a different color.
	• Axes labels correctly show units (e.g., nm, cm⁻¹).
	• You can switch between native units and converted units (where possible) and nothing crashes.
	• Integration test: import → plot two datasets → check that graph_manager has 2 traces, distinct colors, correct axis units.

Phase 3 – Feature 3: Dataset Metadata, Phase & Provenance
Goal: Every dataset knows its basic metadata (object type, phase, source, tags), so later features (search, notes, favorites, projects) can rely on a solid foundation.
Touches:
	• src/domain/datasets/dataset_metadata.*
	• src/data_access/mappers/provider_to_domain.*
	• src/ui/panels/graph_panel/ metadata display
	• docs/dev/data_sources.md
	• tests/unit/test_domain_models.*
Work:
	1. Expand dataset_model.* to include:
		○ object_type (star, planet, moon, molecule, element, “unknown”).
		○ phase (gas, liquid, solid, ice, unknown).
		○ source (local, NIST, HITRAN, MAST, PDS, ESO, etc.).
		○ tags (instrument, telescope, dataset type, etc.).
	2. Implement dataset_metadata.* helpers:
		○ For local imports, try to infer or let the user specify:
			§ Object type.
			§ Phase.
			§ Units (if not in the file).
	3. Add a simple metadata view in graph_panel/:
		○ When a dataset is selected, show a small info box with:
			§ object_type, phase, source, tags, units, filename.
	4. Update tests for domain models and ensure these fields are always present (even if just unknown).
DONE when:
	• Every dataset has a metadata object with the above fields.
	• UI shows metadata clearly for the selected dataset.
	• Tests confirm metadata is never missing and phase is never misused.
	This phase doesn’t add new user-facing “features” but makes all later features cleaner and less buggy.

Phase 4 – Feature 4: Segmented Favorites
Goal: Users can favorite datasets and objects, segmented by category.
Touches:
	• src/domain/ (favorite structures – either per repo or a central favorites manager)
	• src/ui/panels/favorites_panel/
	• src/projects/ (hook favorites into projects later)
	• tests/unit/test_favorites.*
Work:
	1. Create a simple favorites model:
		○ Segments:
			§ datasets
			§ elements
			§ molecules
			§ planets
			§ moons
			§ stars
		○ Backed by a storage layer (likely under data/storage/).
	2. Add UI:
		○ favorites_panel/ for listing favorites.
		○ Buttons in relevant panels (graph, dataset list) to “Add to favorites”.
	3. Persist favorites:
		○ Save favorites to disk.
		○ Reload on app startup.
DONE when:
	• You can mark any dataset as a favorite and see it appear under “Favorite datasets”.
	• Favorites persist across restarts.
	• Favorites are clearly segmented by type.

Phase 5 – Feature 5: Projects / Sessions
Goal: Group datasets, favorites, and notes into named “projects” that you can save and reopen.
Touches:
	• src/projects/ (project_model, project_repo, serializers)
	• src/ui/panels/project_panel/
	• src/domain/datasets/ (link datasets to a project)
	• tests/integration/test_projects.*
	• data/templates/projects/ (a couple of example project files with real data)
Work:
	1. Define project_model.*:
		○ Project name, description.
		○ List of datasets used (by ID/path).
		○ Associated favorites.
		○ Associated notes (references only; notes are stored centrally).
	2. Implement project_repo.* + project_serializer.*:
		○ Save project files to disk (e.g., JSON).
		○ Load them back.
	3. UI:
		○ project_panel/ to:
			§ Create new project.
			§ Open existing project.
			§ Switch between projects.
	4. Integrate with favorites:
		○ When a project is active, it can show project-specific favorites.
DONE when:
	• You can:
		○ Create a project.
		○ Import some datasets.
		○ Mark favorites.
		○ Save the project.
		○ Close the app, reopen, load the project, and see all of that back.

Phase 6 – Feature 6: Notes & Annotations
Goal: Add notes at dataset level and at specific spectral positions, with basic formatting and display on graph + side panel.
Touches:
	• src/notes/ (note_model, note_repo, note_formatter, note_links)
	• src/graphing/overlays/annotation_markers.*
	• src/ui/panels/notes_panel/
	• tests/integration/test_notes_and_annotations.*
Work:
	1. Implement note_model.*:
		○ Text with simple formatting (Markdown-lite: bold, italic, bullet lists).
		○ Optional link to dataset and spectral position (x-value).
	2. Implement note_repo.*:
		○ Save notes to disk.
		○ Load notes globally and within projects.
	3. Implement note_to_dataset.* and note_to_position.*:
		○ Link notes to datasets and specific x-values.
	4. Graph overlays:
		○ When a dataset with notes is plotted, show markers at noted positions.
		○ Tooltips show the note text on hover.
	5. Notes panel:
		○ List all notes for the current project and/or dataset.
		○ Clicking a note highlights the relevant location on the graph.
		○ UI provides controls to avoid clutter (toggle visibility).
DONE when:
	• You can add a note to:
		○ A dataset overall.
		○ A specific x-position on the graph.
	• Notes show on the graph and in the notes panel.
	• Notes persist via projects and across restarts.

Phase 7 – Feature 7: NIST Line Search & Overlays (F3)
Goal: Search NIST ASD for atomic lines and overlay them on existing graphs.
Touches:
	• src/data_access/providers/nist/
	• src/search/providers/line_searcher.*
	• src/search/models/
	• src/graphing/overlays/line_overlays.*
	• src/ui/panels/search_panel/ (NIST mode)
	• tests/integration/test_nist_line_overlay.*
	• data/sample/nist/ (real NIST subsets)
Work:
	1. Implement nist_client.*:
		○ Call NIST ASD (via official endpoints / forms) and retrieve line lists.
	2. Implement nist_parser.*:
		○ Parse responses into structured line data with:
			§ element, ionization state, wavelength/wavenumber, energies, etc.
	3. Implement line_searcher.*:
		○ Accept search_query + search_filter (element, ion, range).
		○ Call nist_client and return structured results.
	4. Graph overlays:
		○ line_overlays.* draws vertical markers or symbols for NIST lines.
		○ On hover, show line details.
	5. UI:
		○ Add NIST line search tab/section in search_panel/.
		○ Allow user to:
			§ Choose element, ion, wavelength range.
			§ Run search.
			§ Overlay selected line sets on current graph.
DONE when:
	• You can:
		○ Load a dataset (local).
		○ Search NIST for lines for a given element/range.
		○ Overlay those lines on the graph.
	• Lines show correct positions and metadata.
	• Test using real NIST subset fixture passes.

Phase 8 – Feature 8: Solar System Search (F4)
Goal: Retrieve and display solar system planet (and ideally moon) spectra/images from real archives (e.g., NASA PDS), and plot them.
Touches:
	• src/data_access/providers/pds/
	• src/search/providers/planet_searcher.*
	• src/domain/planets/ and src/domain/moons/
	• src/ui/panels/search_panel/ (solar system mode)
	• src/graphing/renderers/planets_renderer.*
	• tests/integration/test_solar_system_search.*
	• data/sample/pds/
Work:
	1. Implement pds_client.* and pds_parser.*:
		○ Call appropriate PDS spectral library endpoints.
		○ Retrieve real spectra for at least 1–2 planets and, if possible, 1 moon.
	2. Implement planet_model.* and planet_repo.*:
		○ Store basic planetary properties and link to spectra.
	3. Implement planet_searcher.*:
		○ Search by planet name and wavelength range.
		○ Return candidate spectra.
	4. UI:
		○ Add “Solar System” mode in search_panel/.
		○ Allow selecting a planet → fetch and load its datasets.
		○ Show basic planet info and images (if available).
	5. Graph integration:
		○ Plot planetary spectra on same graph as local data or other sources.
DONE when:
	• You can:
		○ Search for a planet.
		○ Fetch at least one real spectrum for it from PDS.
		○ Plot that spectrum alongside local data.
		○ View basic planetary info and an image (if available).

Phase 9 – Feature 9: Standard Archive Searches (F5 – MAST, HITRAN, etc.)
Goal: Provide a unified “standard search” UI over multiple archives (MAST, HITRAN, maybe ESO) with required filters and saved searches.
Touches:
	• src/data_access/providers/hitran/, mast/, (optionally eso/)
	• src/search/providers/molecule_searcher.*, star_searcher.*
	• src/search/models/search_query.*, search_filter.*, search_result.*
	• src/search/presets/saved_searches.*
	• src/ui/panels/search_panel/ (general mode)
	• tests/integration/test_standard_searches.*
	• data/sample/hitran/, mast/
Work:
	1. Implement common search models:
		○ search_query.* with:
			§ object_type
			§ instrument/telescope
			§ wavelength_range
			§ phase (for molecules)
		○ search_filter.* for additional tags.
	2. Implement providers:
		○ hitran_client.* + hitran_parser.* for gas-phase molecular data.
		○ mast_client.* + mast_parser.* for stellar/space-telescope spectra.
		○ Optionally eso_client.* if needed in v1.
	3. Implement searchers:
		○ molecule_searcher.* for molecules (IR/UV-Vis, with phase filters).
		○ star_searcher.* for stars (Sun and others).
	4. UI:
		○ A clean “Standard Search” panel with:
			§ Object type dropdown.
			§ Instrument/telescope dropdown.
			§ Wavelength range.
			§ Phase selector (for molecules).
		○ Results list that supports:
			§ Loading a dataset into graph.
			§ Adding to favorites.
	5. Saved searches:
		○ Implement saved_searches.*:
			§ Save query + filters under a name.
			§ Reload and re-run easily.
DONE when:
	• You can:
		○ Run a molecule search (e.g., gas-phase CO₂ in some range) via HITRAN, load and plot.
		○ Run a stellar search via MAST, load and plot.
		○ Filter by object type, instrument, wavelength range, and phase (where applicable).
		○ Save a search, restart the app, and re-run it from the saved preset.

Phase 10 – Feature 10: References Panel & Source Linking
Goal: Make all provenance visible and navigable.
Touches:
	• src/domain/references/
	• src/ui/panels/references_panel/
	• src/data_access/mappers/provider_to_domain.* (ensure references attached)
	• docs/references/databases.md, scholarly_refs.md
	• tests/unit/test_references_links.*
Work:
	1. Implement reference_entry.* and reference_repo.*:
		○ Entries for each database and paper.
	2. Ensure each dataset, search result, and project attaches:
		○ A reference ID for its source.
	3. References panel:
		○ List all known references.
		○ Clicking a dataset in the UI shows the associated reference(s).
		○ Each reference has a hyperlink out to the provider docs/page.
DONE when:
	• From any dataset, you can:
		○ Open its source reference.
		○ Click a link to the external archive.
	• References are centralized in a panel.
	• All major sources (HITRAN, MAST, NIST, PDS, ESO, your lab data) appear in docs/references/databases.md.

Phase 11 – Polish, Performance & Packaging
Goal: Make v1 shippable for you and future users.
Touches:
	• All modules, but especially:
		○ src/platform/launcher.*
		○ scripts/build_app.*, package_installer.*
		○ docs/user/getting_started.md, user_guide.md
	• Performance: caching, large file handling.
Work:
	1. Review:
		○ That each phase’s tests exist and pass.
		○ That features match the spec.
	2. Improve caching behavior where needed:
		○ Ensure heavy remote queries are cached and reused.
	3. Packaging:
		○ Provide a way to build:
			§ Windows installer or app bundle.
			§ macOS app bundle.
	4. Documentation:
		○ Update:
			§ getting_started.md
			§ user_guide.md
			§ features.md
		○ Ensure they reflect the actual app behavior.
DONE when:
	• You (as a user) can:
		○ Install/run the app on Windows and macOS without touching the command line.
		○ Import local data, graph, search NIST, pull a planet spectrum, search a molecule/stars, use notes/favorites/projects, and follow references.
	• All tests pass and logs are up to date.

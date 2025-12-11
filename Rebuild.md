App Rebuild Specification (Fresh Start)
0. High-Level Goals
	• Build a local desktop application (no web app) for:
		○ Loading local datasets (any file type, with pluggable importers).
		○ Retrieving real spectra from external archives (no synthetic data).
		○ Graphing and comparing multiple spectra at once.
		○ Searching and visualizing:
			§ Element lines
			§ Molecule spectra (IR, UV-Vis, etc., phase-aware)
			§ Solar system objects (planets, moons)
			§ Standard databases (e.g., NIST, HITRAN, MAST, NASA PDS, ESO)
	• v1 must already support:
		○ Import + export local data.
		○ Graphing.
		○ Line searching (NIST-style).
		○ Solar system object searching.
		○ Standard archive searches (NIST and at least one planetary/library source).
All future features must follow: one feature at a time, fully working before the next.

1. Development Rules & Roles
	1. Feature-by-feature workflow
		○ Implement exactly one feature at a time.
		○ A feature is “done” only when:
			§ UI, data logic, and storage behavior are implemented.
			§ The feature passes its tests (see Section 8).
			§ Documentation and logs are updated (patch log, dev log, features list, wishlist if applicable).
		○ Only then start the next feature.
	2. Role of the human user
		○ The human user:
			§ Provides requirements.
			§ Does light bug testing and feedback.
		○ The user does not:
			§ Write code.
			§ Manage environments.
			§ Build installers.
		○ All instructions and implementation details must be aimed at the coding agents / developers, not at the user.
	3. Language and toolkit freedom
		○ Any programming language/toolkit is allowed as long as:
			§ The app runs locally on Windows and macOS.
			§ It is a desktop application, not a web app.
			§ It can access the internet and local storage.
		○ Examples (not prescriptive): Qt, .NET, native macOS, cross-platform toolkits, etc.
	4. No synthetic data
		○ Absolutely no fake or synthetic data.
		○ All datasets used anywhere in the app (UI demos, tests, examples, documentation) must:
			§ Come from real measurements or real archives.
			§ Be traceable to a source (with a URL/DOI/reference).
		○ A small hard-coded subset of real data is acceptable if:
			§ It is clearly labeled with its origin.
			§ It is actually pulled from a real source (e.g., a subset of NIST, HITRAN, or PDS), not invented.
	5. Online + offline
		○ The app must:
			§ Retrieve data from online archives when needed.
			§ Save/caches data locally so it can be reused offline (within disk space limits).
		○ It should be possible to:
			§ Do meaningful work offline after some data have been cached.

2. Platform & Packaging
	1. OS targets
		○ Required: Windows and macOS.
		○ Linux is optional/“nice to have,” but not required for v1.
	2. Local desktop UI
		○ The UI must be a native desktop application or equivalent (e.g., Qt, Electron-style desktop, .NET/WPF/MAUI, etc.).
		○ No browser-based web app as the primary UI.
	3. Install and run
		○ The implementation must provide:
			§ A simple, user-friendly way to install or run the app on both Windows and macOS.
			§ “One-click” or “double-click” launch (no manual command line required from the user).
		○ All environment setup, dependencies, and packaging are the responsibility of the coding agents/developers.

3. Data Sources, Provenance & Phase Handling
	1. Primary external archives
The app must rely on real, authoritative archives such as:
	• HITRAN / HAPI – Molecular line data for gas-phase molecules (IR, etc.). (hitran.org)
	• MAST (Mashup API) – Space telescope and exoplanet products, including spectra and light curves. (mast.stsci.edu)
	• NIST Atomic Spectra Database (ASD) – Critically evaluated atomic energy levels and spectral lines. (NIST)
	• NASA PDS Geosciences Spectral Library / ECOSTRESS / RELAB – Planetary and laboratory spectral libraries (reflectance, emissivity, etc.). (pds-geosciences.wustl.edu)
	• ESO Science Archive – Ground-based spectra and images, accessed programmatically via VO/TAP interfaces. (archive.eso.org)
	2. Real data only
		○ All remote data must be fetched from these or similarly reputable archives.
		○ Any sample data stored locally in the repo must:
			§ Be clearly sourced (e.g., “subset of NIST ASD line list for Fe I”).
			§ Include reference and link.
	3. In-app referencing
		○ For every dataset, the app must store and display:
			§ Data source name (e.g., “NIST ASD”, “HITRAN”, “PDS Geosciences Node”).
			§ A direct hyperlink to the original source page or API endpoint where possible.
		○ A dedicated References section in the app must:
			§ Aggregate all database references and scholarly references.
			§ Allow one-click navigation to the external sites.
	4. Phase awareness (gas / liquid / solid / ice, etc.)
		○ For molecular and material spectra, the app must track and display the phase of the sample:
			§ Gas
			§ Liquid
			§ Solid
			§ Ice or other relevant states
		○ Requirements:
			§ Phase must be clearly shown in search results and dataset metadata.
			§ Users must be able to filter search results by phase.
			§ The app must never silently mix different phases in a way that could be confused; if overlaid, those traces must be clearly labeled.

4. Core v1 Feature Set
The following capabilities define v1. They should be implemented sequentially (one feature at a time), but all of them must exist in v1.
F1. Local data import & export
	• Import local datasets of many file types:
		○ CSV, TXT, FITS, and other common spectral formats at minimum.
		○ The importer architecture must be pluggable, so new file types can be added later.
	• For unsupported file types:
		○ Provide a clear error or “needs a converter plugin” message.
	• Export:
		○ Allow exporting processed or selected data to at least one common format (e.g., CSV).
		○ Include enough metadata to re-import the data later (units, labels, etc.).
F2. Graphing multiple datasets
	• Plot multiple datasets and types on a single graph (primary mode).
	• Unit handling:
		○ Use the dataset’s native axis as default:
			§ Some datasets will be in wavelength.
			§ Some in wavenumber.
		○ Provide controls to:
			§ Convert axes where possible (e.g., wavelength ↔ wavenumber).
			§ Clearly show current units.
	• Axes:
		○ Default to linear axes.
		○ Provide an option to switch to log scales for analysis.
	• Coloring:
		○ Each dataset must have a distinct color.
		○ Colors must not blend into each other; avoid repeated color assignments within a graph.
	• Visualization customization:
		○ Large, readable, configurable titles.
		○ Configurable axis labels.
		○ Legible legend.
F3. Line searching (NIST-style)
	• Search atomic lines by:
		○ Element and ionization state.
		○ Wavelength (or wavenumber) range.
	• Retrieve data from NIST ASD (or equivalent). (NIST)
	• Plot line positions as overlays on existing graphs.
	• On hover:
		○ Show element, ion state, wavelength/wavenumber, energy levels, and other key metadata where available.
F4. Solar system searching
	• Search and display data for solar system objects:
		○ At minimum: planets; extend to moons where feasible.
	• For each object, retrieve:
		○ Images (UV, IR, visual) where available.
		○ Spectral products where possible (reflectance, emission, etc.).
	• Data must come from real archives (e.g., NASA PDS, relevant mission archives). (pds-geosciences.wustl.edu)
	• Integrate with graphing:
		○ Allow adding planetary/moon spectra onto the main graph.
F5. Standard database searching (NIST, HITRAN, MAST, PDS, ESO)
	• Implement a clean search form with filter options (not a complex query box).
	• For v1, support at least:
		○ NIST atomic line searches (F3).
		○ One molecular/IR source (e.g., HITRAN, or PDS spectral library).
		○ One stellar/space-telescope source (e.g., MAST).
	• Filters required from day one:
		○ Object type (star/planet/moon/molecule/element).
		○ Instrument/telescope.
		○ Wavelength/spectral range.
		○ Phase (for molecules/materials).
	• Saved searches / presets:
		○ Allow users to save searches (e.g., “Jupiter IR 1–5 µm”, “CH₄ gas phase HITRAN”).
		○ Saved searches should be easily reused and editable.

5. Search, Filters, Caching, Favorites, Notes
5.1 Search UI
	• Design:
		○ A clean search form with filter options.
		○ Keep it simple: no complicated query syntax required from the user.
	• Layout (recommended):
		○ Left: Search form + filters.
		○ Right: Results list (tables/cards) and actions (load, preview, favorite).
5.2 Caching
	• Cache all fetched data locally:
		○ Purpose: faster reloads and offline work.
	• Metadata:
		○ Mark in the UI whether a dataset came from:
			§ Cache (offline) vs.
			§ Fresh online query.
	• Provide:
		○ A way to clear or manage cache (size, age, etc.).
5.3 Favorites (segmented)
	• Favorites must be segmented by category:
		○ Favorite datasets.
		○ Favorite elements.
		○ Favorite molecules.
		○ Favorite planets.
		○ Favorite moons.
		○ Favorite stars.
		○ Optional: favorite instruments/searches.
	• Favorites must:
		○ Persist across sessions.
		○ Be easily accessible from a “Favorites” panel.
		○ Be usable as quick inputs to searches and graph overlays.
5.4 Projects / Sessions
	• The app must support projects or sessions, such as:
		○ “Jupiter vs methane lab project”.
	• A project/session stores:
		○ Which data were loaded.
		○ Which notes were created.
		○ Which favorites are associated with that project.
		○ Basic graph configuration (what is displayed).
	• Users should be able to:
		○ Save and reload projects.
		○ Have multiple projects over time.
5.5 Notes & annotations
	• Notes must support some formatting:
		○ At minimum: basic formatting (Markdown-like bold, italics, bullet lists).
	• Notes exist at two levels:
		1. Dataset-level notes (global notes for the entire dataset).
		2. Location-specific notes (attached to particular wavelengths/wavenumbers/features).
	• Display:
		○ Notes should appear both:
			§ As markers on the graph (with hover tooltips).
			§ In a side panel listing notes with clickable entries that highlight the relevant points.
		○ The UI must be designed to avoid clutter:
			§ Allow toggling note visibility.
			§ Option to show only selected or “favorite” notes.

6. Graphing Behavior & UI
	1. Single main graph (v1)
		○ Primary comparison mode is one main graph with multiple overlays.
		○ The design must allow for future features (e.g., multiple graph tabs or multi-panel layouts), but v1 can focus on one main canvas.
	2. Future extensibility
		○ Architecture should allow future:
			§ Additional graphs.
			§ Linked views (e.g., zooming one graph zooms another).
		○ This is not required in v1, but the code should not block it.

7. Domain Libraries
	1. Elements library
		○ All elements:
			§ Names, symbols, common ions.
		○ Spectroscopy-relevant info:
			§ Transition states and energies.
			§ Links into NIST ASD (for lines/levels). (NIST)
		○ Physical info:
			§ Atomic weight; optional additional properties.
	2. Molecules library
		○ Large library of molecules with:
			§ Simple/common names.
			§ Proper/systematic names.
			§ Aliases.
		○ Each molecule linked to:
			§ Its spectra in various archives (gas, solid, liquid, etc.).
			§ 3D models with motion indicating spectral-relevant modes (bending, stretching, etc.).
		○ Phase-aware metadata.
	3. Stars / Planets / Moons / Misc
		○ Catalog entries for:
			§ Stars (with age, distance, classification, color, and composition where available).
			§ Planets (with basic physical properties and atmosphere notes where known).
			§ Moons (with key properties and spectral resources).
		○ Each entry linked to:
			§ The external sources providing its data (MAST, ESO, PDS, etc.).
	4. References library
		○ Centralized registry of:
			§ Database references and URLs (HITRAN, MAST, NIST, PDS, ESO).
			§ Scholarly references for datasets or methods.
		○ Accessible via:
			§ In-app references panel.
			§ Links from any dataset’s detail view.

8. Repo Structure, Branching & Testing
8.1 Repo structure
Use the previously outlined structure (adaptable per language/toolkit):
repo-root/
├── app/
│   ├── ui/
│   ├── graphing/
│   │   ├── chart/
│   │   │   ├── unit_conversion/
│   │   │   └── labeling/
│   │   ├── lines/
│   │   ├── molecules/
│   │   ├── atoms/
│   │   ├── stars/
│   │   ├── planets/
│   │   ├── moons/
│   │   └── misc/
│   ├── searches/
│   │   ├── line_searching/
│   │   ├── molecule_searching/
│   │   ├── planet_searching/
│   │   ├── star_searching/
│   │   └── moon_searching/
│   ├── libraries/
│   │   ├── elements/
│   │   ├── molecules/
│   │   ├── stars/
│   │   ├── planets/
│   │   ├── moons/
│   │   └── misc/
│   ├── references/
│   ├── test/
│   └── documentation/
│       ├── patch_log/
│       ├── dev_log/
│       ├── features/
│       └── wishlist/
└── data/
    ├── retrieval/
    ├── storage/
    ├── analysis/
    ├── references/
    ├── test/
    └── documentation/
        ├── patch_log/
        ├── dev_log/
        ├── features/
        └── wishlist/

8.2 Branching
	• Use a GitHub repo with branches such as:
		○ ui
		○ search
		○ data-analysis
		○ graphing
	• Rule:
		○ Each branch should focus on a narrow slice/feature.
		○ Merge only after:
			§ Feature is complete.
			§ Tests pass.
			§ Documentation and logs updated.
8.3 Testing requirements
	• For every feature, there must be tests that:
		○ Confirm the feature works as intended (load, search, plot, etc.).
		○ Confirm it is properly connected to any other feature that depends on it, or where it provides UI output.
	• At minimum:
		○ Smoke tests:
			§ App launches.
			§ Core workflows (import → graph, search → fetch → graph) do not crash.
		○ Integration tests:
			§ Data retrieval from at least one external source per domain (e.g., one HITRAN, one NIST, one PDS, one MAST query).
			§ Unit conversions behave correctly.
			§ Graph rendering works with multiple datasets and colors.
	• Test data:
		○ Must be real (no synthetic values).
		○ Must be documented and cited in the repo.
8.4 Documentation & logs (keep all)
Every completed feature must update:
	• Patch log – What changed, when, and why.
	• Dev log – Implementation notes, gotchas, and design decisions.
	• Features document – High-level description of available features and how to use them.
	• Wishlist – Future improvements and ideas discovered while implementing the feature.
All of these must be kept; nothing should be dropped “to simplify.”

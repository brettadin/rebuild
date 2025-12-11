import json
from pathlib import Path
from src.data_access.providers.nist.nist_client import NistClient
from src.search.providers.line_searcher import LineSearcher
from src.graphing.overlays.line_overlays import LineOverlay
from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.search.models.line_result import LineResult


def test_nist_search_and_overlay(tmp_path, qtbot):
    # Use sample fixture
    fixture_path = Path('data/sample/nist/sample_nist_lines.json')
    client = NistClient(use_fixture=True, fixture_path=str(fixture_path))
    searcher = LineSearcher(client=client)
    results = searcher.search('Fe')
    assert len(results) >= 1
    r = results[0]
    overlay = LineOverlay(id=r.id, element=r.element, ion=r.ion, x=r.wavelength_nm, metadata=r.metadata)

    # Graph panel - add overlay
    gp = GraphPanel()
    qtbot.addWidget(gp)
    gp.manager.set_line_overlays([overlay])

    # Validate overlay manager updated
    overlays = gp.manager.line_overlay_manager.lines
    assert any(o.id == overlay.id for o in overlays)
    assert any(o.x == 386.0 or o.x == 387.0 for o in overlays)

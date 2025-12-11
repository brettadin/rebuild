from src.ui.panels.search_panel.solar_panel import SolarSystemSearchPanel
from src.ui.panels.graph_panel.graph_panel import GraphPanel
from PySide6.QtWidgets import QWidget
from PySide6.QtTest import QTest
from src.domain.datasets.registry import get_dataset_repo


def test_solar_system_search_and_load(qtbot):
    parent = QWidget()
    sp = SolarSystemSearchPanel(parent=parent, fixture_path='data/sample/pds')
    qtbot.addWidget(sp)

    sp.planet_input.setText('Jupiter')
    sp.on_search()
    assert sp.results_list.count() > 0

    # create a graph panel in parent and register it so the panel can find it
    gp = GraphPanel(parent=parent)
    parent.graph_panel = gp
    qtbot.addWidget(gp)

    # select first result and load
    sp.results_list.setCurrentRow(0)
    sp.on_load_selected()

    # verify a dataset was added to ds repo
    repo = get_dataset_repo()
    ids = repo.list_ids()
    assert len(ids) > 0

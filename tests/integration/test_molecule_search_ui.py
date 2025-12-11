from src.ui.panels.search_panel.molecule_panel import MoleculeSearchPanel
from PySide6.QtWidgets import QInputDialog


def test_molecule_search_panel(qtbot, tmp_path, monkeypatch):
    panel = MoleculeSearchPanel(fixture_path='data/sample/hitran')
    qtbot.addWidget(panel)
    panel.molecule_input.setText('CO2')
    panel.on_search()
    # expect results in list widget
    assert panel.results_list.count() > 0
    # select and load
    panel.results_list.setCurrentRow(0)
    panel.on_load_selected()
    # there should be a dataset in the dataset repo now
    from src.domain.datasets.registry import get_dataset_repo
    ds_repo = get_dataset_repo()
    assert len(ds_repo.list_ids()) > 0

from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.domain.datasets.registry import get_dataset_repo
from src.notes.registry import get_note_repo
from pathlib import Path
import types


def test_add_note_at_and_click_handler(tmp_path, qtbot, monkeypatch):
    # Setup dataset
    ds_repo = get_dataset_repo()
    ds_repo._datasets = {}
    md = DatasetMetadata(units_x='nm', units_y='arb')
    ds = DatasetModel(id='ds1', x=[1.0, 2.0], y=[10, 20], metadata=md)
    ds_repo.add(ds)

    gp = GraphPanel()
    qtbot.addWidget(gp)
    # ensure click-to-create behaviour is enabled for this test
    gp.enable_click_to_create_notes_cb.setChecked(True)
    # add dataset to graph
    gp.manager.add_dataset(ds)

    # call add_note_at directly
    repo = get_note_repo()
    repo.clear()
    gp.add_note_at(2.0, 'Clicked note test', dataset_id='ds1')
    notes = repo.list_for_dataset('ds1')
    assert any(n.text == 'Clicked note test' for n in notes)

    # Now simulate a real canvas click: monkeypatch QInputDialog.getText to return text
    class DummyEvent:
        def __init__(self, xdata, button):
            self.xdata = xdata
            self.button = button
    # monkeypatch getText to return an accepted dialog result
    from PySide6.QtWidgets import QInputDialog
    monkeypatch.setattr(QInputDialog, 'getText', lambda *args, **kwargs: ('clicked via event', True))
    # send a left-click at xdata=1.0
    e = DummyEvent(1.0, 1)
    gp._on_canvas_click(e)
    # Allow scheduled dialog to run
    qtbot.wait(50)
    notes_all = repo.list()
    assert any(n.text == 'clicked via event' for n in notes_all)

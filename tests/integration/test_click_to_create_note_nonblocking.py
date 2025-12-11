from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.domain.datasets.registry import get_dataset_repo
from src.notes.registry import get_note_repo
from PySide6.QtWidgets import QInputDialog


def test_nonblocking_click_prompt(tmp_path, qtbot, monkeypatch):
    ds_repo = get_dataset_repo()
    ds_repo._datasets = {}
    md = DatasetMetadata(units_x='nm', units_y='arb')
    ds = DatasetModel(id='ds1', x=[1.0, 2.0], y=[10, 20], metadata=md)
    ds_repo.add(ds)

    gp = GraphPanel()
    qtbot.addWidget(gp)
    gp.manager.add_dataset(ds)

    # Patch QInputDialog to simulate user entry and ensure it is called asynchronously
    called = {'ok': False}
    def fake_get_text(parent, title, label):
        called['ok'] = True
        return ('Non-blocking note', True)
    monkeypatch.setattr(QInputDialog, 'getText', fake_get_text)

    class DummyEvent:
        def __init__(self, xdata, button):
            self.xdata = xdata
            self.button = button

    e = DummyEvent(1.5, 1)
    # Trigger canvas click; should schedule a dialog via QTimer.singleShot and return immediately
    gp._on_canvas_click(e)
    # Pump the Qt event loop to allow scheduled functions to run
    qtbot.wait(50)
    repo = get_note_repo()
    notes = repo.list()
    assert any(n.text == 'Non-blocking note' for n in notes)

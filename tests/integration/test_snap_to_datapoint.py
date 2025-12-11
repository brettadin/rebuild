from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.domain.datasets.registry import get_dataset_repo
from src.notes.registry import get_note_repo


def test_snap_to_nearest_datapoint(qtbot, monkeypatch):
    repo = get_note_repo()
    repo.clear()
    ds_repo = get_dataset_repo()
    ds_repo._datasets = {}
    md = DatasetMetadata(units_x='nm')
    ds = DatasetModel(id='ds1', x=[1.0, 2.0, 3.0], y=[10, 20, 30], metadata=md)
    ds_repo.add(ds)
    gp = GraphPanel()
    qtbot.addWidget(gp)
    gp.manager.add_dataset(ds)
    gp.enable_click_to_create_notes_cb.setChecked(True)
    # Ensure QInputDialog returns a value so the dialog path exercises add_note_at
    from PySide6.QtWidgets import QInputDialog
    monkeypatch.setattr(QInputDialog, 'getText', lambda *args, **kwargs: ('snapped note', True))
    gp.enable_click_to_create_notes_cb.setChecked(True)
    # simulate click near 2.05 which should snap to 2.0
    class DummyEvent:
        def __init__(self, xdata, button=1):
            self.xdata = xdata
            self.button = button
    e = DummyEvent(2.05, button=1)
    # monkeypatch add_note_at to capture x
    captured = {'x': None}
    def fake_add(x, text, dataset_id=None):
        captured['x'] = x
    gp.add_note_at = fake_add
    gp._on_canvas_click(e)
    # wait for scheduled dialog call (if any) to complete, and for snapping to be applied
    qtbot.wait(50)
    assert abs(captured['x'] - 2.0) < 1e-6

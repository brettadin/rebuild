from src.ui.panels.notes_panel.notes_panel import NotesPanel
from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.notes.registry import get_note_repo
from src.notes.note_model import NoteModel
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.domain.datasets.registry import get_dataset_repo
from PySide6.QtWidgets import QInputDialog


def test_edit_note_ui(monkeypatch, qtbot):
    repo = get_note_repo()
    repo.clear()
    ds_repo = get_dataset_repo()
    ds_repo._datasets = {}
    md = DatasetMetadata(units_x='nm')
    ds = DatasetModel(id='ds1', x=[1.0, 2.0], y=[10, 20], metadata=md)
    ds_repo.add(ds)
    gp = GraphPanel()
    qtbot.addWidget(gp)
    gp._refresh_notes()

    # create a note
    note = NoteModel(id='n1', text='old text', dataset_id='ds1', x=1.0)
    repo.add_note(note)

    npanel = NotesPanel()
    qtbot.addWidget(npanel)
    npanel.refresh_notes_list()

    # monkeypatch getText to return new text
    monkeypatch.setattr(QInputDialog, 'getText', lambda *args, **kwargs: ('new text', True))
    # select first item
    npanel.list_widget.setCurrentRow(0)
    npanel.edit_note()
    updated = repo.get('n1')
    assert updated is not None
    assert updated.text == 'new text'

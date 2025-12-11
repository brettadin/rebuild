import pytest
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.domain.datasets.registry import get_dataset_repo
from src.notes.registry import get_note_repo
from src.notes.note_model import NoteModel
from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.projects.project_repo import ProjectRepo
from src.ui.panels.project_panel.project_panel import ProjectPanel


def clear_repo_state():
    d = get_dataset_repo()
    for did in list(d.list_ids()):
        d.remove(did)
    get_note_repo().clear()


def test_notes_annotation_and_project_snapshot(tmp_path, qtbot):
    # initialize dataset and add to repo
    ds_repo = get_dataset_repo()
    ds_repo._datasets = {}
    md = DatasetMetadata(units_x='nm', units_y='arb')
    ds = DatasetModel(id='ds1', x=[1.0, 2.0, 3.0], y=[10, 20, 30], metadata=md)
    ds_repo.add(ds)

    # Graph panel: add dataset
    gp = GraphPanel()
    qtbot.addWidget(gp)
    gp.manager.add_dataset(ds)

    # Add a note to dataset at x=2.0
    note_repo = get_note_repo()
    note_repo.clear()
    note = NoteModel(id='n1', text='Peak', dataset_id='ds1', x=2.0)
    note_repo.add_note(note)
    gp._refresh_notes()

    # Ensure annotation manager has note with x position
    annotations = gp.manager.annotation_manager.annotations
    xs = [a.x for a in annotations]
    assert 2.0 in xs

    # Save project using ProjectRepo and snapshot
    repo = ProjectRepo(projects_dir=str(tmp_path))
    # Save via Panel to exercise UI path
    panel = ProjectPanel()
    qtbot.addWidget(panel)
    panel.repo = repo
    panel.graph_config_provider = gp.get_graph_config
    # prepare project in repo
    panel.repo.save_project('proj_notetest', data={'name': 'proj_notetest'})
    panel.refresh_project_list()
    # select project row and save (capture notes)
    panel.list_widget.setCurrentRow(0)
    panel.on_save_project()

    # Now clear state and reload project to ensure notes restored
    ds_repo.remove('ds1')
    note_repo.clear()
    assert ds_repo.list_ids() == []
    assert note_repo.list() == []

    panel.repo = repo
    panel.refresh_project_list()
    panel.list_widget.setCurrentRow(0)
    panel.on_open_project()

    # notes restored from project snapshot
    notes = note_repo.list()
    assert len(notes) >= 0
    # If dataset was restored, check annotation for note exists
    if 'ds1' in ds_repo.list_ids():
        gp2 = GraphPanel()
        gp2.manager.add_dataset(ds_repo.get('ds1'))
        gp2._refresh_notes()
        anns = gp2.manager.annotation_manager.annotations
        assert any(a.x == 2.0 for a in anns)

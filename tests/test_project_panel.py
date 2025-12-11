import os
import tempfile
from PySide6 import QtWidgets

from src.ui.panels.project_panel.project_panel import ProjectPanel
from src.projects.project_repo import ProjectRepo


def test_project_panel_create_and_list(qtbot, tmp_path):
    repo = ProjectRepo(projects_dir=str(tmp_path))
    panel = ProjectPanel()
    panel.repo = repo
    qtbot.addWidget(panel)

    # create new project programmatically
    repo.save_project("testproj", {"name": "testproj"})
    panel.refresh_project_list()

    items = [panel.list_widget.item(i).text() for i in range(panel.list_widget.count())]
    assert "testproj" in items


def test_project_panel_delete(qtbot, tmp_path):
    repo = ProjectRepo(projects_dir=str(tmp_path))
    repo.save_project("todelete", {"name": "todelete"})
    panel = ProjectPanel()
    panel.repo = repo
    qtbot.addWidget(panel)
    panel.refresh_project_list()

    # select and delete
    panel.list_widget.setCurrentRow(0)
    panel.on_delete_project()
    panel.refresh_project_list()
    assert panel.list_widget.count() == 0


def test_project_panel_open_emits_signal(qtbot, tmp_path):
    repo = ProjectRepo(projects_dir=str(tmp_path))
    repo.save_project("emitproj", {"name": "emitproj"})
    panel = ProjectPanel()
    panel.repo = repo
    qtbot.addWidget(panel)
    panel.refresh_project_list()

    # connect to signal and assert emission
    with qtbot.waitSignal(panel.projectOpened, timeout=1000) as blocker:
        panel.list_widget.setCurrentRow(0)
        panel.on_open_project()
    assert blocker.args[0] == "emitproj"
    assert blocker.args[1].name == "emitproj"


def test_project_panel_save_and_restore(qtbot, tmp_path):
    # Prepare repos and panel
    from src.domain.datasets.registry import get_dataset_repo
    from src.domain.favorites.favorites_repo import FavoritesRepo
    from src.domain.favorites import registry as fav_registry
    from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata

    ds_repo = get_dataset_repo()
    # clear existing datasets
    ds_repo._datasets = {}

    # create a dataset and add
    md = DatasetMetadata(units_x='nm', units_y='arb', provenance={'path': 'data/sample/test.csv'})
    ds = DatasetModel(id='ds1', x=[1.0, 2.0], y=[10.0, 20.0], metadata=md)
    ds_repo.add(ds)

    # set up favorites repo pointing to tmp file and clear
    fav_repo = FavoritesRepo(storage_file=str(tmp_path / 'fav.json'))
    fav_registry._repo = fav_repo
    fav_repo.clear()
    fav_repo.add_favorite('datasets', 'ds1')

    # create project repo
    repo = ProjectRepo(projects_dir=str(tmp_path))
    panel = ProjectPanel()
    panel.repo = repo
    qtbot.addWidget(panel)

    # create placeholder project entry and refresh
    repo.save_project('proj1', data={'name': 'proj1'})
    panel.refresh_project_list()

    # select and save snapshot
    panel.list_widget.setCurrentRow(0)
    # sanity check: dataset repo has our dataset
    assert 'ds1' in ds_repo.list_ids()
    panel.on_save_project()

    # verify saved file contains datasets snapshot
    import json
    path = tmp_path / 'proj1.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert 'datasets' in data and len(data['datasets']) == 1

    # clear dataset and favorites to simulate fresh state
    ds_repo._datasets = {}
    fav_repo.clear()

    # open project and assert datasets/favorites restored
    panel.list_widget.setCurrentRow(0)
    panel.on_open_project()
    assert 'ds1' in ds_repo.list_ids()
    assert 'ds1' in fav_repo.list('datasets')

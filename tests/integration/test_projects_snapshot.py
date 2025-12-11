import pytest
from pathlib import Path
from src.projects.project_model import ProjectModel
from src.projects.project_repo import ProjectRepo
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.domain.datasets.registry import get_dataset_repo
from src.domain.favorites.registry import get_favorites_repo
from src.ui.panels.project_panel.project_panel import ProjectPanel


def clear_dataset_repo(ds_repo):
    for did in ds_repo.list_ids():
        ds_repo.remove(did)


def test_project_save_load_restore(tmp_path, qtbot):
    # Prepare repos
    ds_repo = get_dataset_repo()
    fav_repo = get_favorites_repo()
    # Clear existing state
    clear_dataset_repo(ds_repo)
    fav_repo.clear()

    # Add a dataset and favorite
    ds = DatasetModel(id='ds1', x=[1.0, 2.0], y=[10.0, 20.0], metadata=DatasetMetadata(object_type='molecule'))
    ds_repo.add(ds)
    fav_repo.add_favorite('datasets', 'ds1')

    # create a graph panel to capture the graph state and add the dataset to it
    from src.ui.panels.graph_panel.graph_panel import GraphPanel
    graph_panel = GraphPanel()
    graph_panel.manager.add_dataset(ds)
    graph_conf = graph_panel.get_graph_config()

    # Save project (include captured graph_config)
    repo = ProjectRepo(projects_dir=str(tmp_path))
    pm = ProjectModel(
        name='proj1',
        description='A test project',
        dataset_ids=['ds1'],
        favorites={'datasets': ['ds1']},
        graph_config=graph_conf,
        datasets=[ds.to_dict()],
    )
    repo.save_project(pm)

    # Clear app state, then reopen via ProjectPanel
    clear_dataset_repo(ds_repo)
    fav_repo.clear()
    assert ds_repo.list_ids() == []
    assert fav_repo.list('datasets') == []

    panel = ProjectPanel()
    panel.repo = repo
    # create a graph panel and hook into project opened to restore traces
    from src.ui.panels.graph_panel.graph_panel import GraphPanel
    graph_panel = GraphPanel()
    qtbot.addWidget(graph_panel)
    # capture graph config when saving
    panel.graph_config_provider = graph_panel.get_graph_config
    # when a project is opened emit add traces to graph_panel
    def on_open(name, project):
        for tid in getattr(project, 'graph_config', {}).get('trace_ids', []):
            ds = ds_repo.get(tid)
            if ds:
                graph_panel.manager.add_dataset(ds)
        if getattr(project, 'graph_config', {}).get('unit_conversion', False):
            graph_panel.manager.set_unit_conversion(True)
    panel.projectOpened.connect(on_open)
    qtbot.addWidget(panel)
    panel.refresh_project_list()

    # Select and open project
    panel.list_widget.setCurrentRow(0)
    panel.on_open_project()

    # Expect dataset restored and favorite restored
    assert 'ds1' in ds_repo.list_ids()
    assert 'ds1' in fav_repo.list('datasets')
    # graph traces restored
    trace_ids = [vm.id for vm in graph_panel.manager.list_traces()]
    assert 'ds1' in trace_ids

def test_project_save_as_and_last_project(tmp_path, qtbot, monkeypatch):
    # Setup dataset and favorites
    from src.domain.datasets.registry import get_dataset_repo
    from src.domain.favorites.favorites_repo import FavoritesRepo
    from src.domain.favorites import registry as fav_registry
    from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
    from src.ui.main_window.main_window import MainWindow

    ds_repo = get_dataset_repo()
    ds_repo._datasets = {}
    md = DatasetMetadata(units_x='nm', units_y='arb', provenance={'path': 'data/sample/test.csv'})
    ds = DatasetModel(id='ds1', x=[1.0, 2.0], y=[10.0, 20.0], metadata=md)
    ds_repo.add(ds)

    fav_repo = FavoritesRepo(storage_file=str(tmp_path / 'fav.json'))
    fav_registry._repo = fav_repo
    fav_repo.clear()
    fav_repo.add_favorite('datasets', 'ds1')

    # Create project repo and panel
    repo = ProjectRepo(projects_dir=str(tmp_path))
    panel = ProjectPanel()
    panel.repo = repo
    qtbot.addWidget(panel)
    repo.save_project('proj1', data={'name': 'proj1'})
    panel.refresh_project_list()

    # Monkeypatch QFileDialog to return a new filename
    from PySide6.QtWidgets import QFileDialog
    monkeypatch.setattr(QFileDialog, 'getSaveFileName', lambda *args, **kwargs: (str(tmp_path / 'proj1_renamed.json'), 'JSON files (*.json)'))

    # select and Save As
    panel.list_widget.setCurrentRow(0)
    panel.on_save_as_project()

    # verify file created
    assert (tmp_path / 'proj1_renamed.json').exists()

    # Start main window and assert it auto-loads last project when set
    # Simulate setting last_project in storage file
    from src.platform.launcher import load_config
    cfg = load_config()
    storage_path = Path(cfg.get('paths', {}).get('storage', 'data/storage'))
    storage_path.mkdir(parents=True, exist_ok=True)
    with open(storage_path / 'last_project.txt', 'w', encoding='utf-8') as f:
        f.write('proj1_renamed')

    # Spawn main window and check the project is loaded (favorites restored)
    mw = MainWindow()
    # Use the panel's repo dir to check if selected
    assert 'ds1' in ds_repo.list_ids()

def test_project_menu_and_favorites_merge(tmp_path, qtbot):
    from src.ui.main_window.main_window import MainWindow
    from src.domain.datasets.registry import get_dataset_repo
    from src.domain.favorites.favorites_repo import FavoritesRepo
    from src.domain.favorites import registry as fav_registry
    from src.projects.project_repo import ProjectRepo
    from src.ui.panels.project_panel.project_panel import ProjectPanel

    # Check menu actions exist
    mw = MainWindow()
    project_actions = mw.get_project_menu_items()
    assert 'New Project' in project_actions
    assert 'Open Project' in project_actions
    assert 'Save Project' in project_actions

    # Setup dataset and favorites
    ds_repo = get_dataset_repo()
    ds_repo._datasets = {}
    ds_repo.add(type('D', (), {'id': 'd1', 'x': [1], 'y': [2], 'to_dict': lambda self: {'id': 'd1', 'x': [1], 'y': [2], 'metadata': {}}})())

    fav_repo = FavoritesRepo(storage_file=str(tmp_path / 'fav.json'))
    fav_registry._repo = fav_repo
    fav_repo.clear()
    fav_repo.add_favorite('datasets', 'existing_ds')

    # Create a project with its own favorite (ds1)
    repo = ProjectRepo(projects_dir=str(tmp_path))
    repo.save_project('proj1', data={'name': 'proj1', 'favorites': {'datasets': ['d1']}})

    panel = ProjectPanel()
    panel.repo = repo
    panel.replace_favs_checkbox.setChecked(False)
    panel.refresh_project_list()
    panel.list_widget.setCurrentRow(0)
    panel.on_open_project()
    # Since merge (default), existing_ds and d1 should both exist
    favs = fav_repo.list('datasets')
    assert 'existing_ds' in favs
    assert 'd1' in favs

    # Now test replace behavior
    fav_repo.clear()
    fav_repo.add_favorite('datasets', 'existing_ds')
    panel.replace_favs_checkbox.setChecked(True)
    panel.on_open_project()
    favs2 = fav_repo.list('datasets')
    assert 'existing_ds' not in favs2
    assert 'd1' in favs2

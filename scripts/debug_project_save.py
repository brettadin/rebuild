import sys, os
sys.path.append(os.getcwd())
from src.domain.datasets.registry import get_dataset_repo
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.projects.project_repo import ProjectRepo
from src.ui.panels.project_panel.project_panel import ProjectPanel
from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication([])
import os, shutil, json

repo_dir = os.path.join(os.getcwd(), 'tmp_debug_proj')
shutil.rmtree(repo_dir, ignore_errors=True)
os.makedirs(repo_dir, exist_ok=True)

repo = get_dataset_repo()
repo._datasets = {}
md = DatasetMetadata(units_x='nm')
ds = DatasetModel(id='ds1', x=[1,2], y=[10,20], metadata=md)
repo.add(ds)
print('after add ds list', repo.list_ids())

project_repo = ProjectRepo(projects_dir=repo_dir)
project_repo.save_project('proj1', data={'name':'proj1'})
panel = ProjectPanel()
panel.repo = project_repo
panel.refresh_project_list()
print('panel repo project list', [panel.list_widget.item(i).text() for i in range(panel.list_widget.count())])
print('panel repo type', type(panel.repo), 'projects_dir', getattr(panel.repo, 'projects_dir', None))

panel.list_widget.setCurrentRow(0)
panel.on_save_project()

path = os.path.join(repo_dir, 'proj1.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print('saved project data keys:', list(data.keys()))
print('datasets in saved project:', data.get('datasets'))
print('dataset_ids in saved project:', data.get('dataset_ids'))

# Also print ds_repo list at point
print('global ds repo list after save:', get_dataset_repo().list_ids())

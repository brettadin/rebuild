from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QHBoxLayout, QFileDialog
from pathlib import Path
from src.notes.registry import get_note_repo
from src.projects.project_repo import ProjectRepo
from src.projects.project_model import ProjectModel


class ProjectPanel(QWidget):
    """UI Panel for creating, listing, opening, and saving projects."""
    projectOpened = QtCore.Signal(str, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repo = ProjectRepo()
        self.graph_config_provider = None
        self.replace_favorites_on_open = False
        self._build_ui()
        self.refresh_project_list()

    def _build_ui(self):
        layout = QVBoxLayout()
        header = QLabel("Projects")
        header.setObjectName("panelHeader")
        layout.addWidget(header)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.btn_new = QPushButton("New Project")
        self.btn_open = QPushButton("Open Project")
        self.btn_save = QPushButton("Save Project")
        self.btn_save_as = QPushButton("Save As...")
        self.btn_delete = QPushButton("Delete Project")
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_open)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_save_as)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_new.clicked.connect(self.on_new_project)
        self.btn_open.clicked.connect(self.on_open_project)
        self.btn_save.clicked.connect(self.on_save_project)
        self.btn_save_as.clicked.connect(self.on_save_as_project)
        self.btn_delete.clicked.connect(self.on_delete_project)
        # Option to replace favorites when opening project
        self.replace_favs_checkbox = QtWidgets.QCheckBox("Replace favorites on open")
        layout.addWidget(self.replace_favs_checkbox)
        self.replace_favs_checkbox.toggled.connect(self.set_replace_favorites_on_open)

    def refresh_project_list(self):
        self.list_widget.clear()
        for p in self.repo.list_projects():
            self.list_widget.addItem(p)

    def on_new_project(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "New Project", "Project name:")
        if ok and name:
            # create empty project and save
            self.repo.save_project(name, data={"name": name, "datasets": [], "favorites": []})
            self.refresh_project_list()

    def on_open_project(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        project_name = item.text()
        project = self.repo.load_project(project_name)
        # attempt to restore snapshot: datasets & favorites
        try:
            from src.domain.datasets.registry import get_dataset_repo
            from src.domain.favorites.registry import get_favorites_repo
            ds_repo = get_dataset_repo()
            fav_repo = get_favorites_repo()
            # Add datasets in project snapshot
            for d in getattr(project, 'datasets', []):
                # reconstruct dataset model
                md = d.get('metadata', {})
                from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
                meta = DatasetMetadata(
                    object_type=md.get('object_type', 'unknown'),
                    phase=md.get('phase', 'unknown'),
                    source=md.get('source', 'local'),
                    tags=md.get('tags', []),
                    units_x=md.get('units_x', ''),
                    units_y=md.get('units_y', ''),
                    provenance=md.get('provenance', None),
                )
                ds = DatasetModel(id=d.get('id', ''), x=d.get('x', []), y=d.get('y', []), metadata=meta)
                ds_repo.add(ds)
            # Restore favorites: either replace (clear then add) or merge (add)
            fav_dict = getattr(project, 'favorites', {}) or {}
            if getattr(self, 'replace_favorites_on_open', False):
                fav_repo.clear()
            for seg, ids in fav_dict.items():
                for ident in ids:
                    fav_repo.add_favorite(seg, ident)
            # Restore notes: project's notes stored as list of dicts
            try:
                from src.notes.registry import get_note_repo
                from src.notes.note_model import NoteModel
                note_repo = get_note_repo()
                note_repo.clear()
                for n in getattr(project, 'notes', []):
                    nm = NoteModel.from_dict(n) if hasattr(NoteModel, 'from_dict') else NoteModel(**n)
                    note_repo.add_note(nm)
            except Exception:
                # Non-fatal, if notes can't be restored we continue
                pass
        except Exception:
            # non-fatal, project loading still happens via signal
            pass
        # emit a signal for other components after restoring datasets/favorites
        self.projectOpened.emit(project_name, project)

    def on_save_project(self):
        # Save the currently-selected project; in a real app we'd capture state
        item = self.list_widget.currentItem()
        if not item:
            return
        name = item.text()
        # Capture datasets and favorites snapshot
        from src.domain.datasets.registry import get_dataset_repo
        from src.domain.favorites.registry import get_favorites_repo
        ds_repo = get_dataset_repo()
        fav_repo = get_favorites_repo()
        dataset_ids = ds_repo.list_ids()
        # debug: ensure this repo contains expected datasets
        # debug logging omitted in production
        datasets = []
        for did in dataset_ids:
            ds = ds_repo.get(did)
            if not ds:
                continue
            datasets.append(ds.to_dict())
        # debug logging omitted in production
        # favorites segments
        fav_segments = ['datasets', 'elements', 'molecules', 'planets', 'moons', 'stars']
        favs = {s: fav_repo.list(s) for s in fav_segments}
        graph_conf = {}
        if hasattr(self, 'graph_config_provider') and callable(self.graph_config_provider):
            try:
                graph_conf = self.graph_config_provider() or {}
            except Exception:
                graph_conf = {}
        project = ProjectModel(
            name=name,
            description=None,
            dataset_ids=dataset_ids,
            favorites=favs,
            graph_config={},
            datasets=datasets,
            notes=[n.to_dict() for n in get_note_repo().list()] if get_note_repo() else [],
        )
        # debug logging omitted in production
        saved_path = self.repo.save_project(project)
        # debug logging omitted in production
        # refresh list in case a new project file was created with the same name
        self.refresh_project_list()
        # Save 'last opened' project in storage by notifying MainWindow via signal

    def on_save_as_project(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        name = item.text()
        # prompt for filename (save under project dir)
        suggested = str(Path(self.repo.projects_dir) / f"{name}.json")
        p = QFileDialog.getSaveFileName(self, "Save Project As", suggested, "JSON files (*.json)")
        filename = p[0] if p and isinstance(p, tuple) else p
        if not filename:
            return
        # Use only the basename for project repo storage
        fname = Path(filename).name
        # Build project snapshot similar to on_save_project
        from src.domain.datasets.registry import get_dataset_repo
        from src.domain.favorites.registry import get_favorites_repo
        ds_repo = get_dataset_repo()
        fav_repo = get_favorites_repo()
        dataset_ids = ds_repo.list_ids()
        datasets = []
        for did in dataset_ids:
            ds = ds_repo.get(did)
            if not ds:
                continue
            datasets.append(ds.to_dict())
        fav_segments = ['datasets', 'elements', 'molecules', 'planets', 'moons', 'stars']
        favs = {s: fav_repo.list(s) for s in fav_segments}
        graph_conf = {}
        if hasattr(self, 'graph_config_provider') and callable(self.graph_config_provider):
            try:
                graph_conf = self.graph_config_provider() or {}
            except Exception:
                graph_conf = {}
        project = ProjectModel(name=name, description=None, dataset_ids=dataset_ids, favorites=favs, graph_config=graph_conf, datasets=datasets)
        # attach notes snapshot
        try:
            from src.notes.registry import get_note_repo
            project.notes = [n.to_dict() for n in get_note_repo().list()]
        except Exception:
            project.notes = []
        self.repo.save_project(project, filename=fname)
        self.refresh_project_list()

    def on_delete_project(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        name = item.text()
        self.repo.delete_project(name)
        self.refresh_project_list()

    def set_replace_favorites_on_open(self, value: bool):
        self.replace_favorites_on_open = bool(value)

    # Backwards-compatible stub (no-op) kept for tests or direct calls
    def project_opened(self, name, project):
        return None


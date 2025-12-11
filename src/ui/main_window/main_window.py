from PySide6.QtWidgets import QMainWindow, QLabel, QMenuBar, QMenu, QDockWidget
from PySide6.QtGui import QAction
from src.ui.panels.project_panel.project_panel import ProjectPanel
from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.domain.datasets.registry import get_dataset_repo
from pathlib import Path
from src.ui.panels.favorites_panel.favorites_panel import FavoritesPanel
from src.platform.launcher import load_config
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rebuild - Spectroscopy")
        self.resize(1000, 700)

        # Basic menu
        menu_bar = QMenuBar(self)
        file_menu = QMenu("File", self)
        new_action = QAction("New", self)
        file_menu.addAction(new_action)
        menu_bar.addMenu(file_menu)

        # Project menu
        project_menu = QMenu("Project", self)
        proj_new_action = QAction("New Project", self)
        proj_open_action = QAction("Open Project", self)
        proj_save_action = QAction("Save Project", self)
        proj_save_as_action = QAction("Save Project As...", self)
        proj_close_action = QAction("Close Project", self)
        project_menu.addAction(proj_new_action)
        project_menu.addAction(proj_open_action)
        project_menu.addAction(proj_save_action)
        project_menu.addAction(proj_save_as_action)
        project_menu.addAction(proj_close_action)
        menu_bar.addMenu(project_menu)
        self.setMenuBar(menu_bar)

        # Content placeholder
        label = QLabel("Welcome to Rebuild (Phase 0) — Minimal app shell")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

        # Project panel dock on the right
        self.project_panel = ProjectPanel(self)
        project_dock = QDockWidget("Projects", self)
        project_dock.setWidget(self.project_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, project_dock)

        # Graph panel in the center
        self.graph_panel = GraphPanel(self)
        self.setCentralWidget(self.graph_panel)

        # Wire project opened signal to restore graph state and datasets
        self.project_panel.projectOpened.connect(self.on_project_opened)
        # Allow project panel to capture current graph config when saving
        self.project_panel.graph_config_provider = self.graph_panel.get_graph_config

        # Connect project menu actions
        proj_new_action.triggered.connect(self.project_panel.on_new_project)
        proj_open_action.triggered.connect(self._menu_open_project)
        proj_save_action.triggered.connect(self._menu_save_project)
        proj_save_as_action.triggered.connect(self.project_panel.on_save_as_project)
        proj_close_action.triggered.connect(self._menu_close_project)

    def _menu_open_project(self):
        # Show the project panel if needed and call open
        self.project_panel.refresh_project_list()
        self.project_panel.on_open_project()

    def _menu_save_project(self):
        self.project_panel.on_save_project()

    def _menu_close_project(self):
        # Close current project: remove traces and clear favorites if desired
        from src.domain.datasets.registry import get_dataset_repo
        from src.domain.favorites.registry import get_favorites_repo
        ds_repo = get_dataset_repo()
        fav_repo = get_favorites_repo()
        # Remove all traces
        for tid in list(ds_repo.list_ids()):
            ds_repo.remove(tid)
        # Reset favorites to empty
        fav_repo.clear()
        # Clear graph panel
        self.graph_panel.manager.traces.clear()
        if self.graph_panel.figure is not None:
            self.graph_panel.figure.gca().clear()
            self.graph_panel.figure.canvas.draw_idle()

        # Favorites panel dock on the left
        self.favorites_panel = FavoritesPanel(self)
        fav_dock = QDockWidget("Favorites", self)
        fav_dock.setWidget(self.favorites_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, fav_dock)

        self.current_project_name = None
        # Try to auto-load last project from storage if configured
        cfg = load_config()
        storage_path = cfg.get('paths', {}).get('storage', 'data/storage')
        last_proj_path = Path(storage_path) / 'last_project.txt'
        try:
            if last_proj_path.exists():
                with open(last_proj_path, 'r', encoding='utf-8') as f:
                    last_name = f.read().strip()
                    if last_name:
                        # refresh the project list then select last project if available
                        self.project_panel.refresh_project_list()
                        proj_index = None
                        for i in range(self.project_panel.list_widget.count()):
                            if self.project_panel.list_widget.item(i).text() == last_name:
                                proj_index = i
                                break
                        if proj_index is not None:
                            self.project_panel.list_widget.setCurrentRow(proj_index)
                            self.project_panel.on_open_project()
        except Exception:
            pass

    def on_project_opened(self, name, project):
        # Ensure datasets are present (ProjectPanel attempts to restore them),
        # then add traces to the graph according to project.graph_config
        ds_repo = get_dataset_repo()
        trace_ids = getattr(project, 'dataset_ids', []) or [d.get('id') for d in getattr(project, 'datasets', [])]
        for tid in trace_ids:
            ds = ds_repo.get(tid)
            if ds:
                self.graph_panel.manager.add_dataset(ds)
        gc = getattr(project, 'graph_config', {}) or {}
        if gc.get('unit_conversion'):
            self.graph_panel.manager.set_unit_conversion(True)
        self.current_project_name = name
        try:
            # Update favorites panel
            self.favorites_panel.set_current_project(project)
            from src.platform.launcher import load_config
            cfg = load_config()
            storage_path = cfg.get('paths', {}).get('storage', 'data/storage')
            Path(storage_path).mkdir(parents=True, exist_ok=True)
            last_proj_path = Path(storage_path) / 'last_project.txt'
            with open(last_proj_path, 'w', encoding='utf-8') as f:
                f.write(str(name))
        except Exception:
            pass

    def get_menu_items(self):
        # Return top-level menu texts
        actions = self.menuBar().actions()
        return [a.text() for a in actions]

    def get_project_menu_items(self):
        # Return list of action texts under Project menu
        for a in self.menuBar().actions():
            if a.text() == 'Project':
                menu = a.menu()
                return [m.text() for m in menu.actions()]
        return []

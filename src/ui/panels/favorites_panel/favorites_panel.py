from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QListWidget, QPushButton, QHBoxLayout, QCheckBox
from src.domain.favorites.registry import get_favorites_repo


class FavoritesPanel(QWidget):
    SEGMENTS = ['datasets', 'elements', 'molecules', 'planets', 'moons', 'stars']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repo = get_favorites_repo()
        self.tabs = QTabWidget()
        self.lists = {}
        self._current_project_favs = None
        self.show_project_only = False
        self.show_project_checkbox = QCheckBox('Project favorites only')
        for seg in self.SEGMENTS:
            list_widget = QListWidget()
            self.lists[seg] = list_widget
            tab = QWidget()
            v = QVBoxLayout()
            btn_layout = QHBoxLayout()
            remove_btn = QPushButton('Remove Selected')
            remove_btn.clicked.connect(lambda _, s=seg: self.remove_selected(s))
            btn_layout.addWidget(remove_btn)
            v.addLayout(btn_layout)
            v.addWidget(list_widget)
            tab.setLayout(v)
            self.tabs.addTab(tab, seg.capitalize())

        lay = QVBoxLayout()
        lay.addWidget(self.show_project_checkbox)
        lay.addWidget(self.tabs)
        self.setLayout(lay)
        self.refresh()

        self.show_project_checkbox.toggled.connect(self._on_toggle_project_only)

    def refresh(self):
        for seg, lw in self.lists.items():
            lw.clear()
            if self.show_project_only and self._current_project_favs:
                for item in self._current_project_favs.get(seg, []):
                    lw.addItem(item)
            else:
                for item in self.repo.list(seg):
                    lw.addItem(item)

    def remove_selected(self, seg: str):
        lw = self.lists[seg]
        item = lw.currentItem()
        if not item:
            return
        identifier = item.text()
        self.repo.remove_favorite(seg, identifier)
        self.refresh()

    def set_current_project(self, project):
        if project is None:
            self._current_project_favs = None
            self.show_project_checkbox.setChecked(False)
        else:
            self._current_project_favs = getattr(project, 'favorites', {}) or {}
        self.refresh()

    def _on_toggle_project_only(self, value: bool):
        self.show_project_only = value
        self.refresh()

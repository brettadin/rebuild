from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QListWidget, QPushButton, QHBoxLayout
from src.domain.favorites.registry import get_favorites_repo


class FavoritesPanel(QWidget):
    SEGMENTS = ['datasets', 'elements', 'molecules', 'planets', 'moons', 'stars']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repo = get_favorites_repo()
        self.tabs = QTabWidget()
        self.lists = {}
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
        lay.addWidget(self.tabs)
        self.setLayout(lay)
        self.refresh()

    def refresh(self):
        for seg, lw in self.lists.items():
            lw.clear()
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

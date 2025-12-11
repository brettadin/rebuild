from PySide6.QtWidgets import QMainWindow, QLabel, QMenuBar, QMenu
from PySide6.QtGui import QAction
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
        self.setMenuBar(menu_bar)

        # Content placeholder
        label = QLabel("Welcome to Rebuild (Phase 0) — Minimal app shell")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

    def get_menu_items(self):
        # Return top-level menu texts
        actions = self.menuBar().actions()
        return [a.text() for a in actions]

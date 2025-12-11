import os
import sys
import pytest

# Ensure `src` is discoverable for imports
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PySide6.QtWidgets import QApplication
from src.ui.main_window.main_window import MainWindow

def test_main_window_constructs():
    # Create a headless QApplication context for widget construction
    app = QApplication.instance() or QApplication([])
    win = MainWindow()
    assert win.windowTitle().startswith("Rebuild"), "Window title should start with 'Rebuild'"
    assert hasattr(win, 'get_menu_items'), "MainWindow should have a get_menu_items helper"
    menus = win.get_menu_items()
    assert "File" in menus
    # cleanup
    if QApplication.instance() is not None:
        QApplication.quit()

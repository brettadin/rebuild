import os
import sys
from pathlib import Path
import yaml

from PySide6.QtWidgets import QApplication
from src.ui.main_window.main_window import MainWindow

def load_config():
    cfg_path = Path(__file__).resolve().parents[2] / "config" / "defaults.yaml"
    if cfg_path.exists():
        with open(cfg_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

def run_app(argv=None):
    argv = argv or sys.argv
    os.environ.setdefault('QT_QPA_PLATFORM', 'xcb' if sys.platform == 'linux' else 'windows')
    app = QApplication(argv)
    main_win = MainWindow()
    main_win.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(run_app())

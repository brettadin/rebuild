import os
import sys
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PySide6.QtWidgets import QApplication
from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.data_access.providers.local.local_file_importer import LocalFileImporter
from src.domain.datasets.registry import get_dataset_repo


def test_graph_panel_selection_updates_metadata(qtbot):
    app = QApplication.instance() or QApplication([])
    gp = GraphPanel()
    importer = LocalFileImporter()
    sample = Path(ROOT) / 'data' / 'sample' / 'local_lab' / 'sample_spectrum.csv'
    ds = importer.import_file(str(sample))
    repo = get_dataset_repo()
    repo.add(ds)
    gp._refresh_list()
    # select the first item
    gp.list_widget.setCurrentRow(0)
    # verify metadata displayed
    assert gp.meta_filename.text() == 'sample_spectrum.csv'
    assert gp.meta_source.text() == 'local'
    # Cleanup
    if QApplication.instance() is not None:
        QApplication.quit()

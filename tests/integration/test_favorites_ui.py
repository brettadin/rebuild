import os
import sys
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PySide6.QtWidgets import QApplication
from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.ui.panels.favorites_panel.favorites_panel import FavoritesPanel
from src.data_access.providers.local.local_file_importer import LocalFileImporter
from src.domain.datasets.registry import get_dataset_repo
from src.domain.favorites.registry import get_favorites_repo


def test_favorite_dataset_via_graph_panel(qtbot):
    app = QApplication.instance() or QApplication([])
    gp = GraphPanel()
    fav = FavoritesPanel()
    importer = LocalFileImporter()
    sample = Path(ROOT) / 'data' / 'sample' / 'local_lab' / 'sample_spectrum.csv'
    ds = importer.import_file(str(sample))
    repo = get_dataset_repo()
    repo.add(ds)
    gp._refresh_list()
    # Select the imported dataset (may not be at index 0 if repo had prior entries)
    idx = None
    for i in range(gp.list_widget.count()):
        if gp.list_widget.item(i).text() == ds.id:
            idx = i
            break
    if idx is None:
        # ensure it is present; if not, add and refresh again
        repo.add(ds)
        gp._refresh_list()
        for i in range(gp.list_widget.count()):
            if gp.list_widget.item(i).text() == ds.id:
                idx = i
                break
    gp.list_widget.setCurrentRow(idx if idx is not None else 0)
    gp.add_to_favorites()
    fav.refresh()
    # favorites repo should contain dataset id
    fav_repo = get_favorites_repo()
    assert ds.id in fav_repo.list('datasets')
    # UI shows item
    found = False
    for i in range(fav.lists['datasets'].count()):
        if fav.lists['datasets'].item(i).text() == ds.id:
            found = True
            break
    assert found
    if QApplication.instance() is not None:
        QApplication.quit()

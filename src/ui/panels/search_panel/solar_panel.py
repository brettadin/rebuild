from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QFormLayout, QMessageBox
from src.search.providers.planet_searcher import PlanetSearcher
from src.domain.planets.registry import get_planet_repo
from src.domain.planets.planet_model import PlanetModel
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.domain.datasets.registry import get_dataset_repo
from src.graphing.core.graph_manager import GraphManager
import uuid


class SolarSystemSearchPanel(QWidget):
    def __init__(self, parent=None, fixture_path: str = "data/sample/pds"):
        super().__init__(parent)
        self.searcher = PlanetSearcher(fixture_path)
        self.results = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        header = QLabel('Solar System (PDS) Spectrum Search')
        layout.addWidget(header)

        form = QFormLayout()
        self.planet_input = QLineEdit()
        form.addRow('Planet Name:', self.planet_input)
        layout.addLayout(form)

        self.search_btn = QPushButton('Search')
        self.load_btn = QPushButton('Load Selected')
        layout.addWidget(self.search_btn)
        layout.addWidget(self.load_btn)

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        self.setLayout(layout)
        self.search_btn.clicked.connect(self.on_search)
        self.load_btn.clicked.connect(self.on_load_selected)

    def on_search(self):
        planet = self.planet_input.text().strip()
        if not planet:
            QMessageBox.warning(self, 'Missing', 'Enter a planet name')
            return
        results = self.searcher.search(planet)
        self.results = results
        self.results_list.clear()
        for r in results:
            self.results_list.addItem(f"{r.planet} — {r.id}")

    def on_load_selected(self):
        sel = self.results_list.currentRow()
        if sel < 0 or sel >= len(self.results):
            return
        r = self.results[sel]
        # Parse spectrum into DatasetModel and add to dataset repo
        ds = None
        if r.spectrum:
            ds_id = f"pds_{r.id}_{str(uuid.uuid4())[:8]}"
            units_x = r.spectrum.get('units_x', 'nm')
            units_y = r.spectrum.get('units_y', '')
            md = DatasetMetadata(object_type='planet', phase='unknown', source='PDS', units_x=units_x, units_y=units_y, filename=r.id)
            ds = DatasetModel(id=ds_id, x=list(r.spectrum.get('x', [])), y=list(r.spectrum.get('y', [])), metadata=md)
            ds_repo = get_dataset_repo()
            ds_repo.add(ds)
            # add to graph
            parent = self.parent()
            graph_panel = None
            if parent and hasattr(parent, 'graph_panel'):
                graph_panel = parent.graph_panel
            if graph_panel and hasattr(graph_panel, 'manager'):
                graph_panel.manager.add_dataset(ds, label=f"{r.planet} ({ds_id})")

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QFormLayout
from src.search.providers.molecule_searcher import MoleculeSearcher
from src.search.models.molecule_result import MoleculeResult
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.domain.datasets.registry import get_dataset_repo
import uuid


class MoleculeSearchPanel(QWidget):
    def __init__(self, parent=None, fixture_path: str = 'data/sample/hitran'):
        super().__init__(parent)
        self.searcher = MoleculeSearcher(fixture_path)
        self.results = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        header = QLabel('Molecule Search (HITRAN-like)')
        layout.addWidget(header)

        form = QFormLayout()
        self.molecule_input = QLineEdit()
        self.phase_input = QLineEdit()
        form.addRow('Molecule:', self.molecule_input)
        form.addRow('Phase (optional):', self.phase_input)
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
        molecule = self.molecule_input.text().strip()
        phase = self.phase_input.text().strip() or None
        results = self.searcher.search(molecule, phase=phase)
        self.results = results
        self.results_list.clear()
        for r in results:
            self.results_list.addItem(f"{r.molecule} ({r.phase}) — {r.id}")

    def on_load_selected(self):
        sel = self.results_list.currentRow()
        if sel < 0 or sel >= len(self.results):
            return
        r: MoleculeResult = self.results[sel]
        ds = None
        if r.spectrum:
            ds_id = f"hitran_{r.id}_{str(uuid.uuid4())[:8]}"
            units_x = r.spectrum.get('units_x', 'nm')
            units_y = r.spectrum.get('units_y', 'arb')
            md = DatasetMetadata(object_type='molecule', phase=(r.phase or 'unknown'), source='HITRAN', units_x=units_x, units_y=units_y, filename=r.id)
            ds = DatasetModel(id=ds_id, x=list(r.spectrum.get('x', [])), y=list(r.spectrum.get('y', [])), metadata=md)
            ds_repo = get_dataset_repo()
            ds_repo.add(ds)
            parent = self.parent()
            graph_panel = None
            if parent and hasattr(parent, 'graph_panel'):
                graph_panel = parent.graph_panel
            if graph_panel and hasattr(graph_panel, 'manager'):
                graph_panel.manager.add_dataset(ds, label=f"{r.molecule} ({ds_id})")

from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QCheckBox, QLabel, QFormLayout, QLineEdit
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.domain.datasets.registry import get_dataset_repo
from src.graphing.core.graph_manager import GraphManager


class GraphPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.repo = get_dataset_repo()
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.manager = GraphManager(self.figure)

        self.list_widget = QListWidget()
        self.add_btn = QPushButton("Add to Graph")
        self.remove_btn = QPushButton("Remove from Graph")
        self.fav_btn = QPushButton("Add to Favorites")
        self.convert_checkbox = QCheckBox("Convert nm to cm^-1")

        lay = QVBoxLayout()
        controls = QHBoxLayout()
        controls.addWidget(self.add_btn)
        controls.addWidget(self.remove_btn)
        controls.addWidget(self.fav_btn)
        controls.addWidget(self.convert_checkbox)
        lay.addLayout(controls)
        lay.addWidget(self.list_widget)
        lay.addWidget(self.canvas)
        self.setLayout(lay)

        self.add_btn.clicked.connect(self.add_selected)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.convert_checkbox.toggled.connect(self.toggle_conversion)
        self.fav_btn.clicked.connect(self.add_to_favorites)

        # Metadata display
        self.metadata_layout = QFormLayout()
        self.meta_object_type = QLineEdit()
        self.meta_phase = QLineEdit()
        self.meta_source = QLineEdit()
        self.meta_units = QLineEdit()
        self.meta_filename = QLineEdit()
        self.meta_object_type.setReadOnly(True)
        self.meta_phase.setReadOnly(True)
        self.meta_source.setReadOnly(True)
        self.meta_units.setReadOnly(True)
        self.meta_filename.setReadOnly(True)
        self.metadata_layout.addRow(QLabel("Object type:"), self.meta_object_type)
        self.metadata_layout.addRow(QLabel("Phase:"), self.meta_phase)
        self.metadata_layout.addRow(QLabel("Source:"), self.meta_source)
        self.metadata_layout.addRow(QLabel("Units (x/y):"), self.meta_units)
        self.metadata_layout.addRow(QLabel("Filename:"), self.meta_filename)
        lay.addLayout(self.metadata_layout)

        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)

        self._refresh_list()

    def _refresh_list(self):
        self.list_widget.clear()
        for id in self.repo.list_ids():
            self.list_widget.addItem(id)

    def add_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        ds = self.repo.get(item.text())
        self.manager.add_dataset(ds, label=item.text())

    def add_to_favorites(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        ds = self.repo.get(item.text())
        if not ds:
            return
        from src.domain.favorites.registry import get_favorites_repo
        fav_repo = get_favorites_repo()
        fav_repo.add_favorite('datasets', ds.id)
        # prefer to keep UI consistent if a favorites panel exists in the app. For now, refresh isn't called.

    def remove_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        self.manager.remove_dataset(item.text())

    def toggle_conversion(self, checked: bool):
        self.manager.set_unit_conversion(checked)

    def on_selection_changed(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        ds = self.repo.get(item.text())
        if not ds:
            return
        md = ds.metadata
        self.meta_object_type.setText(md.object_type)
        self.meta_phase.setText(md.phase)
        self.meta_source.setText(md.source)
        units = f"{md.units_x}/{md.units_y}" if md.units_x or md.units_y else ''
        self.meta_units.setText(units)
        self.meta_filename.setText(md.filename or '')

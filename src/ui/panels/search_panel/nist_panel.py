from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QFormLayout
from src.search.providers.line_searcher import LineSearcher
from src.graphing.overlays.line_overlays import LineOverlay
from src.search.models.line_result import LineResult


class NistSearchPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.searcher = LineSearcher()
        self.results = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        header = QLabel('NIST ASD Line Search')
        layout.addWidget(header)

        form = QFormLayout()
        self.element_input = QLineEdit()
        self.ion_input = QLineEdit()
        self.low_input = QLineEdit()
        self.high_input = QLineEdit()
        form.addRow('Element:', self.element_input)
        form.addRow('Ion (e.g., I, II, III):', self.ion_input)
        form.addRow('Low Wavelength (nm):', self.low_input)
        form.addRow('High Wavelength (nm):', self.high_input)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.search_btn = QPushButton('Search')
        self.overlay_btn = QPushButton('Overlay Selected')
        btn_layout.addWidget(self.search_btn)
        btn_layout.addWidget(self.overlay_btn)
        layout.addLayout(btn_layout)

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        self.setLayout(layout)

        self.search_btn.clicked.connect(self.on_search)
        self.overlay_btn.clicked.connect(self.on_overlay_selected)

    def on_search(self):
        element = self.element_input.text().strip()
        ion = self.ion_input.text().strip()
        low = None
        high = None
        try:
            low = float(self.low_input.text()) if self.low_input.text() else None
        except Exception:
            low = None
        try:
            high = float(self.high_input.text()) if self.high_input.text() else None
        except Exception:
            high = None
        results = self.searcher.search(element, ion, low_wl=low, high_wl=high)
        self.results = results
        self.results_list.clear()
        for r in results:
            label = f"{r.element} {r.ion or ''} — {r.wavelength_nm or r.wavenumber_cm} nm"
            self.results_list.addItem(label)

    def on_overlay_selected(self):
        sel = self.results_list.currentRow()
        if sel < 0 or sel >= len(self.results):
            return
        r: LineResult = self.results[sel]
        overlay = LineOverlay(id=r.id, element=r.element, ion=r.ion, x=r.wavelength_nm, metadata=r.metadata)
        # parent should be main window so it has graph_panel; attempt to find graph_panel
        parent = self.parent()
        if not parent:
            return
        graph_panel = None
        try:
            graph_panel = parent.graph_panel
        except Exception:
            # try main window parent
            if hasattr(parent, 'parent') and parent.parent():
                graph_panel = getattr(parent.parent(), 'graph_panel', None)
        if graph_panel and hasattr(graph_panel, 'manager'):
            # Keep existing overlays and add
            current_overlays = graph_panel.manager.line_overlay_manager.lines if hasattr(graph_panel.manager, 'line_overlay_manager') else []
            new_overlays = current_overlays + [overlay]
            graph_panel.manager.set_line_overlays(new_overlays)
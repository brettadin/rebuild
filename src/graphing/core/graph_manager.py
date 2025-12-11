from typing import Dict, Optional, List
from matplotlib.figure import Figure
from src.graphing.core.dataset_view_model import DatasetViewModel
from src.graphing.core.color_manager import ColorManager
from src.domain.datasets.dataset_model import DatasetModel
from src.graphing.overlays.annotation_markers import AnnotationManager, Annotation


class GraphManager:
    def __init__(self, figure: Optional[Figure] = None):
        self.figure = figure
        self.traces: Dict[str, DatasetViewModel] = {}
        self.color_manager = ColorManager()
        self.unit_conversion = False
        self.annotation_manager = AnnotationManager()

    def add_dataset(self, ds: DatasetModel, label: Optional[str] = None, color: Optional[str] = None):
        if ds.id in self.traces:
            return
        if not color:
            color = self.color_manager.next_color()
        vm = DatasetViewModel(dataset=ds, id=ds.id, label=label or ds.id, color=color)
        self.traces[ds.id] = vm
        if self.figure is not None:
            self._plot_dataset(vm)

    def remove_dataset(self, id: str):
        if id in self.traces:
            del self.traces[id]
            if self.figure is not None:
                self._redraw()

    def list_traces(self) -> List[DatasetViewModel]:
        return list(self.traces.values())

    def _plot_dataset(self, vm: DatasetViewModel):
        ax = self.figure.gca()
        x = vm.get_x()
        y = vm.get_y()
        if self.unit_conversion:
            x = self._convert_units(x, vm.dataset.metadata.units_x)
        ax.plot(x, y, label=vm.label, color=vm.color)
        # draw annotations after plotting
        self.annotation_manager.draw(ax)
        ax.legend()
        self.figure.canvas.draw_idle()

    def _redraw(self):
        ax = self.figure.gca()
        ax.clear()
        for vm in self.traces.values():
            x = vm.get_x()
            y = vm.get_y()
            if self.unit_conversion:
                x = self._convert_units(x, vm.dataset.metadata.units_x)
            ax.plot(x, y, label=vm.label, color=vm.color)
        # draw annotations after plotting
        self.annotation_manager.draw(ax)
        ax.legend()
        self.figure.canvas.draw_idle()

    def set_annotations(self, annotations: List[Annotation]):
        self.annotation_manager.set_annotations(annotations)
        if self.figure is not None:
            self._redraw()

    def set_unit_conversion(self, enabled: bool):
        self.unit_conversion = enabled
        if self.figure is not None:
            self._redraw()

    def _convert_units(self, x_values, units_x):
        # simplistic conversion: nm -> cm^-1 = 1e7 / nm
        if units_x.lower() in ['nm', 'nanometer', 'nanometers']:
            return [1e7 / v if v != 0 else v for v in x_values]
        return x_values

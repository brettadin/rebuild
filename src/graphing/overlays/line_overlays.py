from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import matplotlib.pyplot as plt


@dataclass
class LineOverlay:
    id: str
    element: str
    ion: Optional[str]
    x: Optional[float]
    dataset_id: Optional[str] = None
    energy_lower: Optional[float] = None
    energy_upper: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    visible: bool = True


class LineOverlayManager:
    def __init__(self):
        self.lines: List[LineOverlay] = []

    def set_lines(self, lines: List[LineOverlay]):
        self.lines = lines

    def add_line(self, line: LineOverlay):
        self.lines.append(line)

    def clear(self):
        self.lines = []

    def toggle_visibility(self, id: str, visible: bool):
        for ln in self.lines:
            if ln.id == id:
                ln.visible = visible
                break

    def draw(self, ax: plt.Axes):
        for ln in self.lines:
            if ln.x is None:
                continue
            if not getattr(ln, 'visible', True):
                continue
            ax.axvline(ln.x, color='red', linestyle='-.', linewidth=1)
            ylim = ax.get_ylim()
            y = ylim[1] - (ylim[1] - ylim[0]) * 0.03
            label = f"{ln.element}{(' '+ln.ion) if ln.ion else ''} {ln.x} nm"
            ax.text(ln.x, y, label, rotation=90, verticalalignment='top', fontsize=7, color='darkred')

    def get_nearest_line(self, x: float, tolerance: float = 0.1):
        """Return nearest line overlay to x within tolerance (units same as x)."""
        if x is None:
            return None
        nearest = None
        best_dist = float('inf')
        for ln in self.lines:
            if ln.x is None:
                continue
            d = abs(ln.x - x)
            if d < best_dist and d <= tolerance:
                best_dist = d
                nearest = ln
        return nearest

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import matplotlib.pyplot as plt


@dataclass
class LineOverlay:
    id: str
    element: str
    ion: Optional[str]
    x: Optional[float]
    metadata: Optional[Dict[str, Any]] = None


class LineOverlayManager:
    def __init__(self):
        self.lines: List[LineOverlay] = []

    def set_lines(self, lines: List[LineOverlay]):
        self.lines = lines

    def add_line(self, line: LineOverlay):
        self.lines.append(line)

    def clear(self):
        self.lines = []

    def draw(self, ax: plt.Axes):
        for ln in self.lines:
            if ln.x is None:
                continue
            ax.axvline(ln.x, color='red', linestyle='-.', linewidth=1)
            ylim = ax.get_ylim()
            y = ylim[1] - (ylim[1] - ylim[0]) * 0.03
            label = f"{ln.element}{(' '+ln.ion) if ln.ion else ''} {ln.x} nm"
            ax.text(ln.x, y, label, rotation=90, verticalalignment='top', fontsize=7, color='darkred')

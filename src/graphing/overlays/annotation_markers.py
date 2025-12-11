from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import matplotlib.pyplot as plt


@dataclass
class Annotation:
    id: str
    text: str
    dataset_id: Optional[str] = None
    x: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class AnnotationManager:
    def __init__(self):
        self.annotations: List[Annotation] = []

    def set_annotations(self, annotations: List[Annotation]):
        self.annotations = annotations

    def add_annotation(self, ann: Annotation):
        self.annotations.append(ann)

    def remove_annotation(self, ann_id: str):
        self.annotations = [a for a in self.annotations if a.id != ann_id]

    def draw(self, ax: plt.Axes):
        for ann in self.annotations:
            if ann.x is not None:
                # Draw a vertical line at position x
                ax.axvline(ann.x, color='gray', linestyle='--', linewidth=1)
                # Place small text at top of axes
                ylim = ax.get_ylim()
                y = ylim[1] - (ylim[1] - ylim[0]) * 0.05
                ax.text(ann.x, y, ann.text, rotation=90, verticalalignment='top', fontsize=8, color='gray')


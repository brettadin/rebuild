from dataclasses import dataclass
from typing import Optional
from src.domain.datasets.dataset_model import DatasetModel


@dataclass
class DatasetViewModel:
    dataset: DatasetModel
    id: str
    label: Optional[str] = None
    color: Optional[str] = None
    visible: bool = True

    def get_x(self):
        return self.dataset.x

    def get_y(self):
        return self.dataset.y

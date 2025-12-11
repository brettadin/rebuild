from typing import Dict, Optional
from src.domain.datasets.dataset_model import DatasetModel


class DatasetRepo:
    def __init__(self):
        self._datasets: Dict[str, DatasetModel] = {}

    def add(self, ds: DatasetModel):
        self._datasets[ds.id] = ds

    def get(self, id: str) -> Optional[DatasetModel]:
        return self._datasets.get(id)

    def list_ids(self):
        return list(self._datasets.keys())

    def remove(self, id: str):
        if id in self._datasets:
            del self._datasets[id]

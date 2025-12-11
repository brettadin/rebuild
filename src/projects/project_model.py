from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class ProjectModel:
    name: str
    description: Optional[str] = None
    dataset_ids: List[str] = field(default_factory=list)
    favorites: Dict[str, List[str]] = field(default_factory=dict)
    graph_config: Dict[str, Any] = field(default_factory=dict)
    datasets: List[Dict[str, Any]] = field(default_factory=list)
    notes: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'dataset_ids': self.dataset_ids,
            'favorites': self.favorites,
            'graph_config': self.graph_config,
            'datasets': self.datasets,
            'notes': self.notes,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(
            name=d.get('name', 'Unnamed'),
            description=d.get('description'),
            dataset_ids=d.get('dataset_ids', []),
            favorites=d.get('favorites', {}),
            graph_config=d.get('graph_config', {}),
            datasets=d.get('datasets', []),
            notes=d.get('notes', []),
        )

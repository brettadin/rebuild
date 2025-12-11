from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class NoteModel:
    id: str
    text: str
    dataset_id: Optional[str] = None
    x: Optional[float] = None  # spectral position (wavelength/wavenumber)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'dataset_id': self.dataset_id,
            'x': self.x,
            'created_at': self.created_at,
            'metadata': self.metadata or {},
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(
            id=d.get('id'),
            text=d.get('text', ''),
            dataset_id=d.get('dataset_id'),
            x=d.get('x'),
            created_at=d.get('created_at', datetime.utcnow().isoformat()),
            metadata=d.get('metadata', {}),
        )

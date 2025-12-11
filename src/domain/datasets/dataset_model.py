from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class DatasetMetadata:
    object_type: str = "unknown"  # star, planet, moon, molecule, element, unknown
    phase: str = "unknown"        # gas, liquid, solid, ice, unknown
    source: str = "local"         # local, NIST, HITRAN, etc.
    tags: List[str] = field(default_factory=list)
    units_x: str = ""
    units_y: str = ""
    provenance: Optional[Dict[str, Any]] = None
    filename: Optional[str] = None


@dataclass
class DatasetModel:
    id: str
    x: List[float]
    y: List[float]
    metadata: DatasetMetadata = field(default_factory=DatasetMetadata)

    def size(self) -> int:
        return len(self.x)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "metadata": {
                "object_type": self.metadata.object_type,
                "phase": self.metadata.phase,
                "source": self.metadata.source,
                "tags": self.metadata.tags,
                "units_x": self.metadata.units_x,
                "units_y": self.metadata.units_y,
                "provenance": self.metadata.provenance,
            },
        }

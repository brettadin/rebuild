from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class PlanetResult:
    id: str
    planet: str
    spectrum: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

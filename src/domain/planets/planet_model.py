from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class PlanetModel:
    id: str
    name: str
    metadata: Optional[Dict[str, Any]] = None
    # store a reference to a spectrum (dataset id) or inline spectrum in 'spectrum'
    spectrum: Optional[Dict[str, Any]] = None

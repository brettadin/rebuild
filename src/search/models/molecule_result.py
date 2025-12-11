from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class MoleculeResult:
    id: str
    molecule: str
    phase: Optional[str] = None
    spectrum: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

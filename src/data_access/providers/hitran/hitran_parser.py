from typing import Dict, Any, Optional
from src.search.models.molecule_result import MoleculeResult


def parse_hitran_fixture(raw: Dict[str, Any]) -> Optional[MoleculeResult]:
    if not raw:
        return None
    id = raw.get('id') or raw.get('name') or raw.get('molecule')
    mol = str(raw.get('molecule', ''))
    phase = raw.get('phase', 'unknown')
    spectrum = raw.get('spectrum', None)
    metadata = raw.get('metadata', {})
    return MoleculeResult(id=id, molecule=mol, phase=phase, spectrum=spectrum, metadata=metadata)

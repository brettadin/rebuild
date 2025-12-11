from typing import List
from src.data_access.providers.hitran.hitran_client import HitranClient
from src.data_access.providers.hitran.hitran_parser import parse_hitran_fixture
from src.search.models.molecule_result import MoleculeResult


class MoleculeSearcher:
    def __init__(self, fixture_path: str = 'data/sample/hitran'):
        self.client = HitranClient(fixture_path)

    def search(self, molecule: str, phase: str = None, wavelength_range=None) -> List[MoleculeResult]:
        raw_results = self.client.search_molecule(molecule, phase=phase, wavelength_range=wavelength_range)
        results = []
        for r in raw_results:
            parsed = parse_hitran_fixture(r)
            if parsed:
                results.append(parsed)
        return results

from src.search.providers.molecule_searcher import MoleculeSearcher
from src.search.models.molecule_result import MoleculeResult


def test_hitran_fixture_search():
    ms = MoleculeSearcher(fixture_path='data/sample/hitran')
    results = ms.search('CO2')
    assert isinstance(results, list)
    assert any(r.molecule.lower() == 'co2' for r in results)

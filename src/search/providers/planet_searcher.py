from typing import List, Optional
from src.search.models.planet_result import PlanetResult
from src.data_access.providers.pds.pds_client import PdsClient
from src.data_access.providers.pds.pds_parser import parse_pds_spectrum


class PlanetSearcher:
    def __init__(self, fixture_path: Optional[str] = None):
        self.client = PdsClient(fixture_path)

    def search(self, planet_name: str) -> List[PlanetResult]:
        raw = self.client.fetch_spectrum(planet_name)
        if not raw:
            return []
        # allow multiple entries under a top-level list
        results = []
        if isinstance(raw, list):
            for r in raw:
                ds = parse_pds_spectrum(r)
                if ds:
                    pr = PlanetResult(id=str(r.get('id', r.get('planet', 'planet'))), planet=r.get('planet'), spectrum=r, metadata=r.get('metadata', {}))
                    results.append(pr)
            return results
        # single dict
        ds = parse_pds_spectrum(raw)
        if ds:
            pr = PlanetResult(id=str(raw.get('id') or raw.get('planet')), planet=raw.get('planet'), spectrum=raw, metadata=raw.get('metadata', {}))
            return [pr]
        return []

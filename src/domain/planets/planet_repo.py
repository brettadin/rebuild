from typing import Dict, Optional, List
from src.domain.planets.planet_model import PlanetModel


class PlanetRepo:
    def __init__(self):
        self._planets: Dict[str, PlanetModel] = {}

    def add(self, p: PlanetModel):
        self._planets[p.id] = p

    def get(self, id: str) -> Optional[PlanetModel]:
        return self._planets.get(id)

    def list_ids(self) -> List[str]:
        return list(self._planets.keys())

    def list(self) -> List[PlanetModel]:
        return list(self._planets.values())

from src.domain.planets.planet_repo import PlanetRepo

_repo = PlanetRepo()

def get_planet_repo() -> PlanetRepo:
    return _repo

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Favorites:
    datasets: List[str] = field(default_factory=list)
    elements: List[str] = field(default_factory=list)
    molecules: List[str] = field(default_factory=list)
    planets: List[str] = field(default_factory=list)
    moons: List[str] = field(default_factory=list)
    stars: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, List[str]]:
        return {
            'datasets': self.datasets,
            'elements': self.elements,
            'molecules': self.molecules,
            'planets': self.planets,
            'moons': self.moons,
            'stars': self.stars,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, List[str]]):
        return cls(
            datasets=d.get('datasets', []),
            elements=d.get('elements', []),
            molecules=d.get('molecules', []),
            planets=d.get('planets', []),
            moons=d.get('moons', []),
            stars=d.get('stars', []),
        )

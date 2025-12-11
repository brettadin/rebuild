from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class LineResult:
    id: str
    element: str
    ion: Optional[str]
    wavelength_nm: Optional[float]
    wavenumber_cm: Optional[float]
    energy_lower: Optional[float] = None
    energy_upper: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return {
            'id': self.id,
            'element': self.element,
            'ion': self.ion,
            'wavelength_nm': self.wavelength_nm,
            'wavenumber_cm': self.wavenumber_cm,
            'energy_lower': self.energy_lower,
            'energy_upper': self.energy_upper,
            'metadata': self.metadata or {},
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d.get('id'),
            element=d.get('element'),
            ion=d.get('ion'),
            wavelength_nm=d.get('wavelength_nm'),
            wavenumber_cm=d.get('wavenumber_cm'),
            energy_lower=d.get('energy_lower'),
            energy_upper=d.get('energy_upper'),
            metadata=d.get('metadata', {}),
        )

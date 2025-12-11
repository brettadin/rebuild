from typing import Dict, Any, Optional
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata


def parse_pds_spectrum(raw: Dict[str, Any]) -> Optional[DatasetModel]:
    """Parse a PDS spectrum fixture into a DatasetModel.

    Expected raw format (fixture):
    {
        "id": "jupiter_2020",
        "planet": "Jupiter",
        "x": [ ... ],
        "y": [ ... ],
        "units_x": "nm",
        "units_y": "reflectance",
        "metadata": { ... }
    }
    """
    if not raw or 'x' not in raw or 'y' not in raw:
        return None
    ds_id = raw.get('id') or raw.get('planet')
    units_x = raw.get('units_x', 'nm')
    units_y = raw.get('units_y', '')
    md = DatasetMetadata(object_type='planet', phase='unknown', source='PDS', units_x=units_x, units_y=units_y, filename=raw.get('id'))
    return DatasetModel(id=str(ds_id), x=list(raw.get('x', [])), y=list(raw.get('y', [])), metadata=md)

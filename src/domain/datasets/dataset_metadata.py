from typing import Optional, Dict
from src.domain.datasets.dataset_model import DatasetMetadata
from pathlib import Path


def infer_metadata_from_filepath(path: str) -> DatasetMetadata:
    p = Path(path)
    md = DatasetMetadata()
    md.filename = p.name
    # Heuristics: if file name contains 'planet', 'moon', etc., set object_type
    name_l = p.name.lower()
    if 'planet' in name_l:
        md.object_type = 'planet'
    elif 'moon' in name_l:
        md.object_type = 'moon'
    elif 'star' in name_l:
        md.object_type = 'star'
    elif 'molecule' in name_l or 'hitran' in name_l:
        md.object_type = 'molecule'
    elif 'nist' in name_l:
        md.object_type = 'element'
    else:
        md.object_type = 'unknown'
    return md


def infer_units_from_header(header_line: Optional[str]) -> Dict[str, str]:
    units_x = ''
    units_y = ''
    if not header_line:
        return {"units_x": units_x, "units_y": units_y}
    h = header_line.lower()
    if 'wavelength' in h or 'nm' in h or 'nm,' in h:
        units_x = 'nm'
    if 'wavenumber' in h or 'cm^-1' in h or 'cm-1' in h:
        units_x = 'cm^-1'
    if 'flux' in h or 'intensity' in h:
        units_y = 'flux'
    if 'reflectance' in h:
        units_y = 'reflectance'
    # default guess
    return {"units_x": units_x, "units_y": units_y}

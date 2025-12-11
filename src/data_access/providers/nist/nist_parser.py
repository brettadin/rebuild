from typing import List, Dict, Any
from src.search.models.line_result import LineResult


def parse_nist_lines(raw: List[Dict[str, Any]]) -> List[LineResult]:
    """Parse a NIST response into LineResult objects.

    If raw is a list of dicts (fixture), map fields; if raw is text, attempt a naive parse.
    """
    results = []
    # Fixture style: list of dicts with keys matching LineResult.
    if not raw:
        return results
    # If first element is dict-like with 'element' key
    if isinstance(raw[0], dict) and 'element' in raw[0]:
        for i, r in enumerate(raw):
            lr = LineResult(
                id=str(r.get('id', f'nist{i}')),
                element=r.get('element', ''),
                ion=r.get('ion'),
                wavelength_nm=r.get('wavelength_nm'),
                wavenumber_cm=r.get('wavenumber_cm'),
                energy_lower=r.get('energy_lower'),
                energy_upper=r.get('energy_upper'),
                metadata=r.get('metadata', {}),
            )
            results.append(lr)
        return results
    # If text, naive parse: find lines like 'Element Ion Wavelength: 123.45 nm'
    text = ''.join(raw)
    for i, line in enumerate(text.splitlines()):
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        # try find wavelength like 123.456 nm
        if 'nm' in line:
            try:
                # find number before 'nm'
                idx = line.index('nm')
                num_part = line[:idx].strip().split()[-1]
                wl = float(num_part)
            except Exception:
                wl = None
            # element is first token
            element = parts[0]
            ion = parts[1] if len(parts) > 1 else None
            lr = LineResult(id=f'nist{i}', element=element, ion=ion, wavelength_nm=wl, wavenumber_cm=None)
            results.append(lr)
    return results

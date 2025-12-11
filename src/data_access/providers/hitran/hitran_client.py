import json
from typing import Optional, List, Dict, Any
from pathlib import Path


class HitranClient:
    def __init__(self, fixture_path: Optional[str] = None):
        self.fixture_path = fixture_path

    def search_molecule(self, molecule_name: str, phase: Optional[str] = None, wavelength_range: Optional[List[float]] = None) -> List[Dict[str, Any]]:
        """Search for molecules in fixture files matching molecule_name. Returns a list of raw fixture dicts.

        Fixture mode: scan fixture_path for json files containing 'molecule' matching molecule_name (case-insensitive).
        """
        results = []
        if not self.fixture_path:
            return results
        p = Path(self.fixture_path)
        if not p.exists():
            return results
        files = [p] if p.is_file() else list(p.iterdir())
        for f in files:
            if f.suffix.lower() not in ['.json', '.csv']:
                continue
            try:
                content = json.loads(f.read_text()) if f.suffix.lower() == '.json' else None
            except Exception:
                content = None
            if not content:
                continue
            m = content.get('molecule', '')
            if molecule_name.lower() in str(m).lower():
                # optional phase filter
                if phase and content.get('phase', '').lower() != phase.lower():
                    pass
                else:
                    results.append(content)
        return results

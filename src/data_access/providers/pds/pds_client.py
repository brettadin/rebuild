import json
from typing import Optional
from pathlib import Path


class PdsClient:
    def __init__(self, fixture_path: Optional[str] = None):
        self.fixture_path = fixture_path

    def fetch_spectrum(self, planet_name: str):
        """Fetch a planetary spectrum for planet_name.

        If a fixture_path is set, attempt to load the fixture file whose name
        contains the planet_name (case-insensitive). Otherwise, not implemented.
        """
        if self.fixture_path:
            # search for fixture file that contains planet_name
            p = Path(self.fixture_path)
            if not p.exists():
                return None
            # allow single json fixture or a folder
            if p.is_dir():
                for f in p.iterdir():
                    if planet_name.lower() in f.name.lower() and f.suffix in ['.json', '.csv']:
                        if f.suffix == '.json':
                            try:
                                return json.loads(f.read_text())
                            except Exception:
                                return None
            else:
                try:
                    return json.loads(p.read_text())
                except Exception:
                    return None
        # live fetching not implemented for now
        return None

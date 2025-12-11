from typing import Dict, Any, List, Optional


class NistClient:
    """Simple NIST ASD client wrapper.

    This client will attempt to call a configured NIST endpoint. For tests we allow
    passing a local fixture by setting use_fixture=True and fixture_path.
    """

    def __init__(self, base_url: Optional[str] = None, use_fixture: bool = False, fixture_path: Optional[str] = None):
        self.base_url = base_url or 'https://physics.nist.gov/cgi-bin/ASD/lines1.pl'
        self.use_fixture = use_fixture
        self.fixture_path = fixture_path
        self._session = None

    def search_lines_online(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        # In production, this should perform a GET or POST according to NIST form.
        try:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
        except Exception:
            return []
        # create a session with retries for robust calls
        if self._session is None:
            s = requests.Session()
            retry = Retry(total=2, backoff_factor=0.3, status_forcelist=(500, 502, 504))
            adapter = HTTPAdapter(max_retries=retry)
            s.mount('http://', adapter)
            s.mount('https://', adapter)
            s.headers.update({'User-Agent': 'RebuildSpectro/1.0 (+https://github.com/brettadin/rebuild)'})
            self._session = s
        r = self._session.get(self.base_url, params=params, timeout=10)
        r.raise_for_status()
        return [r.text]

    def search_lines(self, element: str, ion: str = '', low_wl: Optional[float] = None, high_wl: Optional[float] = None) -> List[Dict[str, Any]]:
        # For tests, we can read a local JSON/line list fixture file
        if self.use_fixture and self.fixture_path:
            import json
            with open(self.fixture_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        params = {
            'spectrum': f"{element} {ion}" if ion else element,
            'ol': '1',
            'format': 'ASCII',
        }
        if low_wl is not None:
            params['low_wl'] = low_wl
        if high_wl is not None:
            params['high_wl'] = high_wl
        try:
            return self.search_lines_online(params)
        except Exception:
            # Fallback to empty list
            return []

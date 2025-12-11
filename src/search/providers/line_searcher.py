from typing import List, Optional
from src.data_access.providers.nist.nist_client import NistClient
from src.data_access.providers.nist.nist_parser import parse_nist_lines
from src.search.models.line_result import LineResult


class LineSearcher:
    def __init__(self, client: Optional[NistClient] = None):
        self.client = client or NistClient()

    def search(self, element: str, ion: str = '', low_wl: Optional[float] = None, high_wl: Optional[float] = None) -> List[LineResult]:
        raw = self.client.search_lines(element=element, ion=ion, low_wl=low_wl, high_wl=high_wl)
        return parse_nist_lines(raw)

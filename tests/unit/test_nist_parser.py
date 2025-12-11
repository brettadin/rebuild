from src.data_access.providers.nist.nist_parser import parse_nist_lines
import json
from pathlib import Path


def test_parse_nist_fixture(tmp_path):
    # load sample fixture
    path = Path('data/sample/nist/sample_nist_lines.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    results = parse_nist_lines(data)
    assert len(results) == 2
    r0 = results[0]
    assert r0.element == 'Fe'
    assert r0.wavelength_nm == 386.0

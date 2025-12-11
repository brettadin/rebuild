import os
import sys
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.data_access.providers.local.local_file_importer import LocalFileImporter


def test_import_export_round_trip(tmp_path):
    importer = LocalFileImporter()
    sample = Path(ROOT) / 'data' / 'sample' / 'local_lab' / 'sample_spectrum.csv'
    ds = importer.import_file(str(sample))
    assert ds is not None
    assert ds.size() == 5
    # Export to temp file
    outp = tmp_path / 'out.csv'
    importer.export_csv(ds, str(outp))
    # Re-import and compare dimensions
    ds2 = importer.import_file(str(outp))
    assert ds2.size() == ds.size()

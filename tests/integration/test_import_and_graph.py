import os
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.data_access.providers.local.local_file_importer import LocalFileImporter
from src.domain.datasets.registry import get_dataset_repo
from src.graphing.core.graph_manager import GraphManager
from matplotlib.figure import Figure


def test_import_and_graph_two_files(tmp_path):
    importer = LocalFileImporter()
    repo = get_dataset_repo()
    sample1 = Path(ROOT) / 'data' / 'sample' / 'local_lab' / 'sample_spectrum.csv'
    sample2 = Path(ROOT) / 'data' / 'sample' / 'local_lab' / 'sample_spectrum2.csv'

    ds1 = importer.import_file(str(sample1), units_x='nm', units_y='flux')
    ds2 = importer.import_file(str(sample2), units_x='nm', units_y='flux')
    repo.add(ds1)
    repo.add(ds2)

    fig = Figure()
    gm = GraphManager(figure=fig)
    gm.add_dataset(ds1, label='s1')
    gm.add_dataset(ds2, label='s2')
    traces = gm.list_traces()
    assert len(traces) == 2
    assert traces[0].color != traces[1].color
    # Test unit conversion
    gm.set_unit_conversion(True)
    # ensure converted x-values differ from original x-values for nm->cm^-1
    x_original = ds1.x[0]
    x_converted = gm._convert_units([x_original], ds1.metadata.units_x)[0]
    assert x_converted != x_original

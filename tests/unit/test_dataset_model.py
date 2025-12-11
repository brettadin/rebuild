from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata


def test_dataset_model_basics():
    md = DatasetMetadata(object_type='molecule', phase='gas', source='local', units_x='nm', units_y='flux')
    ds = DatasetModel(id='test', x=[1.0, 2.0], y=[10.0, 20.0], metadata=md)
    assert ds.size() == 2
    d = ds.to_dict()
    assert d['metadata']['units_x'] == 'nm'
    assert d['metadata']['units_y'] == 'flux'

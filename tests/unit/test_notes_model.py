from src.notes.note_model import NoteModel


def test_note_model_to_from_dict():
    n = NoteModel(id='n1', text='Test', dataset_id='ds1', x=123.45)
    d = n.to_dict()
    assert d['id'] == 'n1'
    assert d['text'] == 'Test'
    assert d['dataset_id'] == 'ds1'
    assert d['x'] == 123.45
    n2 = NoteModel.from_dict(d)
    assert n2.id == 'n1'
    assert n2.text == 'Test'
    assert n2.dataset_id == 'ds1'
    assert n2.x == 123.45

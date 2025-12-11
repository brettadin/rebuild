from pathlib import Path
from src.notes.note_repo import NoteRepo
from src.notes.note_model import NoteModel


def test_note_repo_add_remove(tmp_path):
    f = tmp_path / 'notes.json'
    repo = NoteRepo(storage_file=str(f))
    repo.clear()
    n1 = NoteModel(id='n1', text='First', dataset_id='ds1', x=100)
    n2 = NoteModel(id='n2', text='Second', dataset_id='ds1', x=200)
    repo.add_note(n1)
    repo.add_note(n2)
    assert len(repo.list()) == 2
    repo.remove_note('n1')
    assert repo.get('n1') is None
    assert repo.get('n2') is not None
    r2 = NoteRepo(storage_file=str(f))
    assert r2.get('n2') is not None

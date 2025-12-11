from pathlib import Path
from src.notes.note_repo import NoteRepo
from src.platform.launcher import load_config

_repo: NoteRepo = None

def get_note_repo() -> NoteRepo:
    global _repo
    if _repo is None:
        cfg = load_config()
        storage_path = cfg.get('paths', {}).get('storage', 'data/storage')
        note_file_name = cfg.get('paths', {}).get('notes_file', 'notes.json')
        note_path = Path(storage_path) / note_file_name
        _repo = NoteRepo(storage_file=str(note_path))
    return _repo

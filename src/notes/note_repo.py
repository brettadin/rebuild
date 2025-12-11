import json
from pathlib import Path
from typing import List, Optional
from src.notes.note_model import NoteModel


class NoteRepo:
    def __init__(self, storage_file: Optional[str] = None):
        self._storage_file = Path(storage_file) if storage_file else None
        self._notes: List[NoteModel] = []
        if self._storage_file:
            self._storage_file.parent.mkdir(parents=True, exist_ok=True)
            self.load()

    def load(self):
        if self._storage_file and self._storage_file.exists():
            try:
                with open(self._storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f) or []
                    self._notes = [NoteModel.from_dict(n) for n in data]
            except Exception:
                self._notes = []

    def save(self):
        if not self._storage_file:
            return
        with open(self._storage_file, 'w', encoding='utf-8') as f:
            json.dump([n.to_dict() for n in self._notes], f, indent=2)

    def add_note(self, note: NoteModel):
        self._notes.append(note)
        self.save()

    

    def remove_note(self, note_id: str):
        self._notes = [n for n in self._notes if n.id != note_id]
        self.save()

    def update_note(self, note: NoteModel):
        for i, n in enumerate(self._notes):
            if n.id == note.id:
                self._notes[i] = note
                self.save()
                return
        # If not found, append
        self._notes.append(note)
        self.save()

    def list(self):
        return list(self._notes)

    def list_for_dataset(self, dataset_id: str):
        return [n for n in self._notes if n.dataset_id == dataset_id]

    def get(self, note_id: str):
        for n in self._notes:
            if n.id == note_id:
                return n
        return None

    def clear(self):
        self._notes = []
        self.save()

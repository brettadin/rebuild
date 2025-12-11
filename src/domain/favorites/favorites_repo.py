import json
from typing import Optional
from pathlib import Path
from src.domain.favorites.favorites_model import Favorites


class FavoritesRepo:
    def __init__(self, storage_file: Optional[str] = None):
        self._storage_file = Path(storage_file) if storage_file else None
        self._favorites = Favorites()
        if self._storage_file:
            self._storage_file.parent.mkdir(parents=True, exist_ok=True)
            self.load()

    def load(self):
        if self._storage_file and self._storage_file.exists():
            try:
                with open(self._storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._favorites = Favorites.from_dict(data)
            except Exception:
                self._favorites = Favorites()

    def save(self):
        if not self._storage_file:
            return
        with open(self._storage_file, 'w', encoding='utf-8') as f:
            json.dump(self._favorites.to_dict(), f, indent=2)

    def add_favorite(self, segment: str, identifier: str):
        seg = getattr(self._favorites, segment)
        if identifier not in seg:
            seg.append(identifier)
            self.save()

    def remove_favorite(self, segment: str, identifier: str):
        seg = getattr(self._favorites, segment)
        if identifier in seg:
            seg.remove(identifier)
            self.save()

    def list(self, segment: str):
        return getattr(self._favorites, segment)

    def clear(self):
        self._favorites = Favorites()
        self.save()

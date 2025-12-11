from pathlib import Path
from src.domain.favorites.favorites_repo import FavoritesRepo
from src.platform.launcher import load_config

_repo: FavoritesRepo = None

def get_favorites_repo() -> FavoritesRepo:
    global _repo
    if _repo is None:
        cfg = load_config()
        storage_path = cfg.get('paths', {}).get('storage', 'data/storage')
        fav_file_name = cfg.get('paths', {}).get('favorites_file', 'favorites.json')
        fav_path = Path(storage_path) / fav_file_name
        _repo = FavoritesRepo(storage_file=str(fav_path))
    return _repo

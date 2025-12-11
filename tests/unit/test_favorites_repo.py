import tempfile
from pathlib import Path
from src.domain.favorites.favorites_repo import FavoritesRepo


def test_favorites_repo_add_remove(tmp_path):
    file = tmp_path / 'favorites.json'
    repo = FavoritesRepo(storage_file=str(file))
    repo.clear()
    repo.add_favorite('datasets', 'ds1')
    repo.add_favorite('datasets', 'ds2')
    assert 'ds1' in repo.list('datasets')
    assert 'ds2' in repo.list('datasets')
    repo.remove_favorite('datasets', 'ds1')
    assert 'ds1' not in repo.list('datasets')
    # reload from file
    repo2 = FavoritesRepo(storage_file=str(file))
    assert 'ds2' in repo2.list('datasets')

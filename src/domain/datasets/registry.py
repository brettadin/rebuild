from src.domain.datasets.dataset_repo import DatasetRepo

_repo = DatasetRepo()

def get_dataset_repo() -> DatasetRepo:
    return _repo

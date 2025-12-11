from src.projects.project_repo import ProjectRepo
from src.projects.project_model import ProjectModel


def test_save_load_list_delete(tmp_path):
    repo = ProjectRepo(projects_dir=str(tmp_path))
    pm = ProjectModel(name="example", description="desc")
    path = repo.save_project(pm)
    assert path
    projects = repo.list_projects()
    assert "example" in projects
    loaded = repo.load_project("example")
    assert loaded.name == "example"
    deleted = repo.delete_project("example")
    assert deleted
    assert "example" not in repo.list_projects()

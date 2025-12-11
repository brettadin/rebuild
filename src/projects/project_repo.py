import json
from pathlib import Path
from typing import Optional, List, Union, Dict, Any
from src.projects.project_model import ProjectModel


class ProjectRepo:
    def __init__(self, projects_dir: Optional[str] = None):
        self.projects_dir = Path(projects_dir or 'data/templates/projects')
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    def save_project(self, project: Union[ProjectModel, str], data: Optional[Dict[str, Any]] = None, filename: Optional[str] = None) -> str:
        """Save a project.

        Accepts either a ProjectModel instance or a project name with a data dict.
        """
        if isinstance(project, ProjectModel):
            proj = project
        else:
            proj = ProjectModel.from_dict(data or {"name": str(project)})
        if not filename:
            filename = f"{proj.name.replace(' ', '_')}.json"
        path = self.projects_dir / filename
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(proj.to_dict(), f, indent=2)
        return str(path)

    def load_project(self, name_or_path: str) -> ProjectModel:
        p = Path(name_or_path)
        if not p.exists():
            p = self.projects_dir / f"{name_or_path}.json"
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return ProjectModel.from_dict(data)

    def list_projects(self) -> List[str]:
        projects = []
        for p in self.projects_dir.glob('*.json'):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict) and 'name' in data:
                    projects.append(p.stem)
            except Exception:
                continue
        return projects

    def delete_project(self, name_or_path: str) -> bool:
        p = Path(name_or_path)
        if not p.exists():
            p = self.projects_dir / f"{name_or_path}.json"
        if p.exists():
            p.unlink()
            return True
        return False

from typing import Protocol

from app.domain.entities.project import ProjectEntity


class ProjectRepository(Protocol):
    def list_projects(self) -> list[ProjectEntity]: ...
    def create_project(self, project: ProjectEntity) -> ProjectEntity: ...

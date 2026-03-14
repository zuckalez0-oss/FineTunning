from app.domain.entities.project import ProjectEntity
from app.domain.interfaces.project_repository import ProjectRepository
from app.schemas.project import ProjectCreateSchema


class CreateProjectUseCase:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    def execute(self, payload: ProjectCreateSchema) -> ProjectEntity:
        if not payload.name.strip():
            raise ValueError("Project name is required.")

        return self.repository.create_project(
            ProjectEntity(name=payload.name.strip(), description=payload.description)
        )

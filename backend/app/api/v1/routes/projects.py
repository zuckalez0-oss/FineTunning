from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_project_repository
from app.application.use_cases.create_project import CreateProjectUseCase
from app.domain.interfaces.project_repository import ProjectRepository
from app.schemas.project import ProjectCreateSchema


router = APIRouter()


@router.get("/")
def list_projects(
    repository: ProjectRepository = Depends(get_project_repository),
) -> dict[str, list[dict[str, object]]]:
    return {"data": [project.model_dump() for project in repository.list_projects()]}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreateSchema,
    repository: ProjectRepository = Depends(get_project_repository),
) -> dict[str, dict[str, object]]:
    try:
        created = CreateProjectUseCase(repository=repository).execute(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return {"data": created.model_dump()}

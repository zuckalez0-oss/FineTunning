from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_persona_repository
from app.application.use_cases.manage_personas import ManagePersonasUseCase
from app.domain.interfaces.persona_repository import PersonaRepository
from app.schemas.persona import PersonaCreateSchema, PersonaUpdateSchema


router = APIRouter()


@router.get("/")
def list_personas(
    repository: PersonaRepository = Depends(get_persona_repository),
) -> dict[str, list[dict[str, object]]]:
    use_case = ManagePersonasUseCase(repository=repository)
    personas = use_case.execute()
    return {"data": [persona.model_dump() for persona in personas]}


@router.get("/{persona_id}")
def get_persona(
    persona_id: str,
    repository: PersonaRepository = Depends(get_persona_repository),
) -> dict[str, dict[str, object]]:
    use_case = ManagePersonasUseCase(repository=repository)
    persona = use_case.obter_persona_por_id(persona_id)
    if persona is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found.")
    return {"data": persona.model_dump()}


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_persona(
    payload: PersonaCreateSchema,
    repository: PersonaRepository = Depends(get_persona_repository),
) -> dict[str, dict[str, object]]:
    use_case = ManagePersonasUseCase(repository=repository)
    created = use_case.adicionar_persona(payload)
    return {"data": created.model_dump()}


@router.put("/{persona_id}")
def update_persona(
    persona_id: str,
    payload: PersonaUpdateSchema,
    repository: PersonaRepository = Depends(get_persona_repository),
) -> dict[str, dict[str, object]]:
    use_case = ManagePersonasUseCase(repository=repository)
    updated = use_case.atualizar_persona(persona_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found.")
    return {"data": updated.model_dump()}


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(
    persona_id: str,
    repository: PersonaRepository = Depends(get_persona_repository),
) -> None:
    use_case = ManagePersonasUseCase(repository=repository)
    deleted = use_case.deletar_persona(persona_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found.")

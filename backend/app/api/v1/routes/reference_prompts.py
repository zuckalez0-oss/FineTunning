from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_reference_prompt_repository
from app.application.use_cases.manage_reference_prompts import (
    ManageReferencePromptsUseCase,
)
from app.domain.interfaces.reference_prompt_repository import ReferencePromptRepository
from app.schemas.reference_prompt import (
    ReferencePromptCreateSchema,
    ReferencePromptUpdateSchema,
)


router = APIRouter()


@router.get("/")
def listar_prompts_referencia(
    repository: ReferencePromptRepository = Depends(get_reference_prompt_repository),
) -> dict[str, list[dict[str, object]]]:
    use_case = ManageReferencePromptsUseCase(repository=repository)
    prompts = use_case.listar_prompts_referencia()
    return {"data": [prompt.model_dump() for prompt in prompts]}


@router.get("/{prompt_id}")
def obter_prompt_por_id(
    prompt_id: str,
    repository: ReferencePromptRepository = Depends(get_reference_prompt_repository),
) -> dict[str, dict[str, object]]:
    use_case = ManageReferencePromptsUseCase(repository=repository)
    prompt = use_case.obter_prompt_por_id(prompt_id)
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found.")
    return {"data": prompt.model_dump()}


@router.post("/", status_code=status.HTTP_201_CREATED)
def adicionar_prompt_referencia(
    payload: ReferencePromptCreateSchema,
    repository: ReferencePromptRepository = Depends(get_reference_prompt_repository),
) -> dict[str, dict[str, object]]:
    use_case = ManageReferencePromptsUseCase(repository=repository)
    created = use_case.adicionar_prompt_referencia(payload)
    return {"data": created.model_dump()}


@router.put("/{prompt_id}")
def atualizar_prompt_referencia(
    prompt_id: str,
    payload: ReferencePromptUpdateSchema,
    repository: ReferencePromptRepository = Depends(get_reference_prompt_repository),
) -> dict[str, dict[str, object]]:
    use_case = ManageReferencePromptsUseCase(repository=repository)
    updated = use_case.atualizar_prompt_referencia(prompt_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found.")
    return {"data": updated.model_dump()}


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_prompt_referencia(
    prompt_id: str,
    repository: ReferencePromptRepository = Depends(get_reference_prompt_repository),
) -> None:
    use_case = ManageReferencePromptsUseCase(repository=repository)
    deleted = use_case.deletar_prompt_referencia(prompt_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found.")

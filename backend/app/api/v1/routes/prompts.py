from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_llm_gateway,
    get_prompt_builder_service,
    get_prompt_repository,
)
from app.application.services.prompt_builder_service import PromptBuilderService
from app.application.use_cases.generate_prompt import GeneratePromptUseCase
from app.application.use_cases.improve_prompt import ImprovePromptUseCase
from app.domain.interfaces.llm_gateway import LlmGateway
from app.domain.interfaces.prompt_repository import PromptRepository
from app.schemas.prompt import PromptCreateSchema, PromptImproveSchema


router = APIRouter()


@router.get("/")
def list_prompts(
    repository: PromptRepository = Depends(get_prompt_repository),
) -> dict[str, list[dict[str, object]]]:
    return {"data": [prompt.model_dump() for prompt in repository.list_prompts()]}


@router.post("/", status_code=status.HTTP_201_CREATED)
def generate_prompt(
    payload: PromptCreateSchema,
    repository: PromptRepository = Depends(get_prompt_repository),
    llm_gateway: LlmGateway = Depends(get_llm_gateway),
    builder: PromptBuilderService = Depends(get_prompt_builder_service),
) -> dict[str, dict[str, object]]:
    use_case = GeneratePromptUseCase(
        repository=repository,
        llm_gateway=llm_gateway,
        prompt_builder=builder,
    )
    created = use_case.execute(payload)
    return {"data": created.model_dump()}


@router.post("/{prompt_id}/improve")
def improve_prompt(
    prompt_id: str,
    payload: PromptImproveSchema,
    repository: PromptRepository = Depends(get_prompt_repository),
    llm_gateway: LlmGateway = Depends(get_llm_gateway),
) -> dict[str, dict[str, object]]:
    try:
        improved = ImprovePromptUseCase(repository=repository, llm_gateway=llm_gateway).execute(
            prompt_id=prompt_id,
            instruction=payload.instruction,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return {"data": improved}

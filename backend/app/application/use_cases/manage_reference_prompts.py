from app.domain.entities.reference_prompt import ReferencePromptEntity
from app.domain.interfaces.reference_prompt_repository import ReferencePromptRepository
from app.schemas.reference_prompt import (
    ReferencePromptCreateSchema,
    ReferencePromptUpdateSchema,
)


class ManageReferencePromptsUseCase:
    def __init__(self, repository: ReferencePromptRepository) -> None:
        self.repository = repository

    def listar_prompts_referencia(self) -> list[ReferencePromptEntity]:
        return self.repository.listar_prompts_referencia()

    def obter_prompt_por_id(self, prompt_id: str) -> ReferencePromptEntity | None:
        return self.repository.obter_prompt_por_id(prompt_id)

    def adicionar_prompt_referencia(
        self, payload: ReferencePromptCreateSchema
    ) -> ReferencePromptEntity:
        return self.repository.adicionar_prompt_referencia(
            ReferencePromptEntity(**payload.model_dump())
        )

    def atualizar_prompt_referencia(
        self, prompt_id: str, payload: ReferencePromptUpdateSchema
    ) -> ReferencePromptEntity | None:
        novos_dados = payload.model_dump(exclude_none=True)
        return self.repository.atualizar_prompt_referencia(prompt_id, novos_dados)

    def deletar_prompt_referencia(self, prompt_id: str) -> bool:
        return self.repository.deletar_prompt_referencia(prompt_id)

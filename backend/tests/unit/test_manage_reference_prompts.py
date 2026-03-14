from app.application.use_cases.manage_reference_prompts import (
    ManageReferencePromptsUseCase,
)
from app.domain.entities.reference_prompt import ReferencePromptEntity
from app.schemas.reference_prompt import ReferencePromptCreateSchema


class InMemoryReferencePromptRepository:
    def __init__(self) -> None:
        self._items: list[ReferencePromptEntity] = []

    def listar_prompts_referencia(self) -> list[ReferencePromptEntity]:
        return self._items

    def obter_prompt_por_id(self, prompt_id: str) -> ReferencePromptEntity | None:
        return next((item for item in self._items if item.id == prompt_id), None)

    def adicionar_prompt_referencia(
        self, prompt: ReferencePromptEntity
    ) -> ReferencePromptEntity:
        created = prompt.model_copy(update={"id": "ref-1"})
        self._items.append(created)
        return created

    def atualizar_prompt_referencia(
        self, prompt_id: str, novos_dados: dict[str, object]
    ) -> ReferencePromptEntity | None:
        current = self.obter_prompt_por_id(prompt_id)
        if current is None:
            return None
        updated = current.model_copy(update=novos_dados)
        self._items = [updated if item.id == prompt_id else item for item in self._items]
        return updated

    def deletar_prompt_referencia(self, prompt_id: str) -> bool:
        before = len(self._items)
        self._items = [item for item in self._items if item.id != prompt_id]
        return len(self._items) < before


def test_can_add_reference_prompt() -> None:
    use_case = ManageReferencePromptsUseCase(InMemoryReferencePromptRepository())

    created = use_case.adicionar_prompt_referencia(
        ReferencePromptCreateSchema(
            nome="Prompt SEO",
            descricao="Prompt base para SEO",
            conteudo_prompt="Crie um plano de SEO para blog tecnico.",
            categoria="marketing",
        )
    )

    assert created.id == "ref-1"
    assert created.nome == "Prompt SEO"

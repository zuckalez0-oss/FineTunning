from app.application.services.prompt_builder_service import PromptBuilderService
from app.domain.entities.prompt import PromptEntity
from app.domain.interfaces.llm_gateway import LlmGateway
from app.domain.interfaces.prompt_repository import PromptRepository
from app.schemas.prompt import PromptCreateSchema


class GeneratePromptUseCase:
    def __init__(
        self,
        repository: PromptRepository,
        llm_gateway: LlmGateway,
        prompt_builder: PromptBuilderService,
    ) -> None:
        self.repository = repository
        self.llm_gateway = llm_gateway
        self.prompt_builder = prompt_builder

    def execute(self, payload: PromptCreateSchema) -> PromptEntity:
        instruction = self.prompt_builder.build_instruction(
            title=payload.title,
            idea=payload.idea,
            category=payload.category,
        )
        generated_content = self.llm_gateway.generate_text(instruction)

        prompt = PromptEntity(
            title=payload.title,
            content=generated_content,
            tags=payload.tags,
            category=payload.category or "Engineering",
            project_id=payload.project_id,
        )
        return self.repository.create_prompt(prompt)

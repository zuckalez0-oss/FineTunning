from app.domain.interfaces.llm_gateway import LlmGateway
from app.domain.interfaces.prompt_repository import PromptRepository


class ImprovePromptUseCase:
    def __init__(self, repository: PromptRepository, llm_gateway: LlmGateway) -> None:
        self.repository = repository
        self.llm_gateway = llm_gateway

    def execute(self, prompt_id: str, instruction: str) -> dict[str, str]:
        original = self.repository.get_prompt_by_id(prompt_id)
        if original is None:
            raise ValueError("Prompt not found.")

        improved_text = self.llm_gateway.generate_text(
            "Melhore o prompt abaixo mantendo o objetivo central.\n"
            f"Prompt original:\n{original.content}\n"
            f"Instrucao adicional:\n{instruction}"
        )

        updated = original.model_copy(update={"content": improved_text})
        self.repository.update_prompt(prompt_id=prompt_id, prompt=updated)
        return {
            "original_prompt": original.content,
            "refined_prompt": improved_text,
        }

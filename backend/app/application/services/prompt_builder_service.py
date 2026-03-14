from app.application.services.tag_detection_service import TagDetectionService


class PromptBuilderService:
    def __init__(self, tag_detection_service: TagDetectionService) -> None:
        self.tag_detection_service = tag_detection_service

    def build_instruction(self, title: str, idea: str, category: str | None) -> str:
        detected_tags = self.tag_detection_service.detect(idea=idea, category=category)
        tags_hint = ", ".join(detected_tags) if detected_tags else "sem tags"
        normalized_category = category or "general"
        return (
            "Voce e um especialista em engenharia de prompts.\n"
            f"Titulo: {title}\n"
            f"Categoria: {normalized_category}\n"
            f"Contexto do usuario: {idea}\n"
            f"Tags sugeridas: {tags_hint}\n"
            "Entregue um prompt claro, estruturado e pronto para uso."
        )

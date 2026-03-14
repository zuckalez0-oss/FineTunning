from app.domain.entities.persona import PersonaEntity
from app.domain.interfaces.persona_repository import PersonaRepository


class LoadPersonaUseCase:
    def __init__(self, repository: PersonaRepository) -> None:
        self.repository = repository

    def execute(self) -> list[PersonaEntity]:
        return self.repository.list_personas()

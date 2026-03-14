from app.domain.entities.persona import PersonaEntity
from app.domain.interfaces.persona_repository import PersonaRepository
from app.schemas.persona import PersonaCreateSchema, PersonaUpdateSchema


class ManagePersonasUseCase:
    def __init__(self, repository: PersonaRepository) -> None:
        self.repository = repository

    def listar_personas(self) -> list[PersonaEntity]:
        return self.repository.list_personas()

    def execute(self) -> list[PersonaEntity]:
        return self.listar_personas()

    def obter_persona_por_id(self, persona_id: str) -> PersonaEntity | None:
        return self.repository.get_persona_by_id(persona_id)

    def adicionar_persona(self, payload: PersonaCreateSchema) -> PersonaEntity:
        return self.repository.add_persona(PersonaEntity(id="", **payload.model_dump()))

    def atualizar_persona(
        self, persona_id: str, payload: PersonaUpdateSchema
    ) -> PersonaEntity | None:
        return self.repository.update_persona(
            persona_id, payload.model_dump(exclude_none=True)
        )

    def deletar_persona(self, persona_id: str) -> bool:
        return self.repository.delete_persona(persona_id)

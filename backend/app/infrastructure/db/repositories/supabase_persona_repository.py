from app.domain.entities.persona import PersonaEntity
from app.infrastructure.db.supabase_client import get_supabase_client


class SupabasePersonaRepository:
    table_name = "persona_profiles"

    def list_personas(self) -> list[PersonaEntity]:
        response = get_supabase_client().table(self.table_name).select("*").order("name").execute()
        return [PersonaEntity(**self._normalize_record(record)) for record in response.data or []]

    def get_persona_by_id(self, persona_id: str) -> PersonaEntity | None:
        response = (
            get_supabase_client()
            .table(self.table_name)
            .select("*")
            .eq("id", persona_id)
            .execute()
        )
        if not response.data:
            return None
        return PersonaEntity(**self._normalize_record(response.data[0]))

    def add_persona(self, persona: PersonaEntity) -> PersonaEntity:
        payload = {
            "name": persona.name,
            "description": persona.description,
            "system_prompt": persona.system_prompt,
            "category": persona.category,
            "auto_detect_tags": persona.auto_detect_tags,
        }
        response = get_supabase_client().table(self.table_name).insert(payload).execute()
        return PersonaEntity(**self._normalize_record(response.data[0]))

    def update_persona(
        self, persona_id: str, novos_dados: dict[str, object]
    ) -> PersonaEntity | None:
        payload = self._normalize_payload(novos_dados)
        response = (
            get_supabase_client()
            .table(self.table_name)
            .update(payload)
            .eq("id", persona_id)
            .execute()
        )
        if not response.data:
            return None
        return PersonaEntity(**self._normalize_record(response.data[0]))

    def delete_persona(self, persona_id: str) -> bool:
        response = (
            get_supabase_client()
            .table(self.table_name)
            .delete()
            .eq("id", persona_id)
            .execute()
        )
        return response.data is not None

    def _normalize_record(self, record: dict[str, object]) -> dict[str, object]:
        return {
            "id": record.get("id"),
            "name": record.get("name"),
            "description": record.get("description"),
            "system_prompt": record.get("system_prompt"),
            "example_behavior": None,
            "category": record.get("category"),
            "auto_detect_tags": record.get("auto_detect_tags") or [],
        }

    def _normalize_payload(self, data: dict[str, object]) -> dict[str, object]:
        field_map = {
            "name": "name",
            "description": "description",
            "system_prompt": "system_prompt",
            "category": "category",
            "auto_detect_tags": "auto_detect_tags",
        }
        return {field_map[key]: value for key, value in data.items() if key in field_map}

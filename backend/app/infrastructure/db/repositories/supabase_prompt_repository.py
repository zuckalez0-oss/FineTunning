from app.domain.entities.prompt import PromptEntity
from app.infrastructure.db.supabase_client import get_supabase_client


class SupabasePromptRepository:
    table_name = "prompts"

    def list_prompts(self) -> list[PromptEntity]:
        response = (
            get_supabase_client().table(self.table_name).select("*").order("created_at", desc=True).execute()
        )
        return [PromptEntity.from_record(record) for record in response.data or []]

    def get_prompt_by_id(self, prompt_id: str) -> PromptEntity | None:
        response = (
            get_supabase_client().table(self.table_name).select("*").eq("id", prompt_id).execute()
        )
        if not response.data:
            return None
        return PromptEntity.from_record(response.data[0])

    def create_prompt(self, prompt: PromptEntity) -> PromptEntity:
        payload = prompt.model_dump(exclude_none=True)
        response = get_supabase_client().table(self.table_name).insert(payload).execute()
        return PromptEntity.from_record(response.data[0])

    def update_prompt(self, prompt_id: str, prompt: PromptEntity) -> PromptEntity | None:
        payload = prompt.model_dump(exclude_none=True)
        response = (
            get_supabase_client().table(self.table_name).update(payload).eq("id", prompt_id).execute()
        )
        if not response.data:
            return None
        return PromptEntity.from_record(response.data[0])

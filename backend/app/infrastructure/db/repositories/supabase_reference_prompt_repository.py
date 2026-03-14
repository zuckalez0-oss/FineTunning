from app.domain.entities.reference_prompt import ReferencePromptEntity
from app.infrastructure.db.supabase_client import get_supabase_client


class SupabaseReferencePromptRepository:
    table_name = "prompts_referencia"

    def listar_prompts_referencia(self) -> list[ReferencePromptEntity]:
        response = (
            get_supabase_client().table(self.table_name).select("*").order("data_criacao", desc=True).execute()
        )
        return [ReferencePromptEntity(**record) for record in response.data or []]

    def obter_prompt_por_id(self, prompt_id: str) -> ReferencePromptEntity | None:
        response = (
            get_supabase_client().table(self.table_name).select("*").eq("id", prompt_id).execute()
        )
        if not response.data:
            return None
        return ReferencePromptEntity(**response.data[0])

    def adicionar_prompt_referencia(
        self, prompt: ReferencePromptEntity
    ) -> ReferencePromptEntity:
        payload = prompt.model_dump(exclude_none=True)
        response = get_supabase_client().table(self.table_name).insert(payload).execute()
        return ReferencePromptEntity(**response.data[0])

    def atualizar_prompt_referencia(
        self, prompt_id: str, novos_dados: dict[str, object]
    ) -> ReferencePromptEntity | None:
        response = (
            get_supabase_client()
            .table(self.table_name)
            .update(novos_dados)
            .eq("id", prompt_id)
            .execute()
        )
        if not response.data:
            return None
        return ReferencePromptEntity(**response.data[0])

    def deletar_prompt_referencia(self, prompt_id: str) -> bool:
        response = (
            get_supabase_client().table(self.table_name).delete().eq("id", prompt_id).execute()
        )
        return response.data is not None

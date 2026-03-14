from app.domain.entities.project import ProjectEntity
from app.infrastructure.db.supabase_client import get_supabase_client


class SupabaseProjectRepository:
    table_name = "projects"

    def list_projects(self) -> list[ProjectEntity]:
        response = (
            get_supabase_client().table(self.table_name).select("*").order("created_at", desc=True).execute()
        )
        return [ProjectEntity(**record) for record in response.data or []]

    def create_project(self, project: ProjectEntity) -> ProjectEntity:
        payload = project.model_dump(exclude_none=True)
        response = get_supabase_client().table(self.table_name).insert(payload).execute()
        return ProjectEntity(**response.data[0])

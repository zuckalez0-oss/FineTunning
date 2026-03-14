from datetime import datetime

from pydantic import BaseModel


class ProjectEntity(BaseModel):
    id: str | None = None
    name: str
    description: str | None = None
    created_at: datetime | None = None

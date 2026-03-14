from datetime import datetime

from pydantic import BaseModel, Field


class ContextSnapshotEntity(BaseModel):
    id: str | None = None
    prompt_id: str
    summary: str
    tags: list[str] = Field(default_factory=list)
    created_at: datetime | None = None

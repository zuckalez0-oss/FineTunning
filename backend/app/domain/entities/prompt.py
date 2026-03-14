from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PromptEntity(BaseModel):
    id: str | None = None
    title: str = "Untitled Prompt"
    content: str
    tags: list[str] = Field(default_factory=list)
    category: str = "Engineering"
    project_id: str | None = None
    role: str = "user"
    token_estimate: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "PromptEntity":
        return cls(**record)

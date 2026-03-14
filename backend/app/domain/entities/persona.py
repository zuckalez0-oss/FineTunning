from pydantic import BaseModel, Field


class PersonaEntity(BaseModel):
    id: str | None = None
    name: str
    system_prompt: str
    auto_detect_tags: list[str] = Field(default_factory=list)
    description: str | None = None
    category: str | None = None
    example_behavior: str | None = None

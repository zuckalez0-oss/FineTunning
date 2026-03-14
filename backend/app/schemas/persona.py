from pydantic import BaseModel, Field


class PersonaResponseSchema(BaseModel):
    id: str
    name: str
    system_prompt: str
    auto_detect_tags: list[str] = Field(default_factory=list)
    description: str | None = None
    category: str | None = None
    example_behavior: str | None = None


class PersonaCreateSchema(BaseModel):
    name: str
    description: str | None = None
    system_prompt: str
    category: str | None = None
    example_behavior: str | None = None


class PersonaUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    system_prompt: str | None = None
    category: str | None = None
    example_behavior: str | None = None

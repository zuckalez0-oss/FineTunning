from pydantic import BaseModel, Field


class PromptCreateSchema(BaseModel):
    title: str = "Untitled Prompt"
    idea: str
    tags: list[str] = Field(default_factory=list)
    category: str | None = "Engineering"
    project_id: str | None = None


class PromptImproveSchema(BaseModel):
    instruction: str

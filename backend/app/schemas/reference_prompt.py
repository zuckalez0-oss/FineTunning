from pydantic import BaseModel


class ReferencePromptCreateSchema(BaseModel):
    nome: str
    descricao: str | None = None
    conteudo_prompt: str
    categoria: str | None = None


class ReferencePromptUpdateSchema(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    conteudo_prompt: str | None = None
    categoria: str | None = None

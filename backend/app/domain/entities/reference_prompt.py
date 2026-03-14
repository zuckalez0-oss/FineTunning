from datetime import datetime

from pydantic import BaseModel


class ReferencePromptEntity(BaseModel):
    id: str | None = None
    nome: str
    descricao: str | None = None
    conteudo_prompt: str
    categoria: str | None = None
    data_criacao: datetime | None = None

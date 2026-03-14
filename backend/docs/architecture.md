# PromptMaster Backend Architecture

## Objective

Unificar a logica de negocio para CLI e Web usando uma mesma camada de aplicacao, com Supabase como fonte central de prompts de referencia e personas.

## Layers

- `api/`: entrypoints HTTP e adaptadores de request/response.
- `application/`: casos de uso, servicos compartilhados e regras de menu.
- `domain/`: entidades e contratos de repositorio/gateway.
- `infrastructure/`: adaptadores Supabase e Gemini.
- `schemas/`: modelos de entrada/saida da API.
- `cli/`: interface de terminal consumindo a mesma camada de aplicacao.

## Shared Flow

1. CLI ou Web chama um caso de uso.
2. O caso de uso usa um repositorio (`Supabase`) e, quando necessario, um gateway LLM.
3. O resultado volta padronizado para a interface consumidora.

## Main Endpoints

- `GET /api/v1/reference-prompts`
- `GET /api/v1/reference-prompts/{id}`
- `POST /api/v1/reference-prompts`
- `PUT /api/v1/reference-prompts/{id}`
- `DELETE /api/v1/reference-prompts/{id}`
- `GET /api/v1/personas`
- `GET /api/v1/personas/{id}`
- `POST /api/v1/personas`
- `PUT /api/v1/personas/{id}`
- `DELETE /api/v1/personas/{id}`

## Diagnosed Failure Points

- Environment drift between terminal, IDE and broken `.venv`.
- External clients initialized at import time, causing startup crashes with poor diagnostics.
- Missing dependencies in the active terminal environment.
- Mixed responsibilities in the previous routes/services with direct provider usage.

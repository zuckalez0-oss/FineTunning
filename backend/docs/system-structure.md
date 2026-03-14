# Suggested Project Structure

```text
prompt-master/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  │  ├─ dependencies.py
│  │  │  └─ v1/
│  │  │     ├─ router.py
│  │  │     └─ routes/
│  │  │        ├─ health.py
│  │  │        ├─ personas.py
│  │  │        ├─ projects.py
│  │  │        ├─ prompts.py
│  │  │        └─ reference_prompts.py
│  │  ├─ application/
│  │  │  ├─ services/
│  │  │  └─ use_cases/
│  │  ├─ cli/
│  │  ├─ core/
│  │  ├─ domain/
│  │  ├─ infrastructure/
│  │  ├─ schemas/
│  │  └─ main.py
│  ├─ docs/
│  ├─ migrations/
│  ├─ scripts/
│  ├─ tests/
│  └─ pyproject.toml
├─ frontend/
│  ├─ src/
│  │  ├─ app/
│  │  ├─ components/
│  │  ├─ hooks/
│  │  ├─ lib/
│  │  ├─ services/
│  │  └─ types/
│  └─ package.json
└─ docker-compose.yml
```

## Reuse Rule

- CLI and Web never talk directly to Supabase.
- Both consume shared use cases in the backend.
- Frontend services only call the backend HTTP API.

from fastapi import APIRouter

from app.api.v1.routes import health, personas, projects, prompts, reference_prompts


api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(
    reference_prompts.router,
    prefix="/reference-prompts",
    tags=["reference-prompts"],
)
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(personas.router, prefix="/personas", tags=["personas"])

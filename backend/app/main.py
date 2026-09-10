from fastapi import FastAPI

from backend.app.api.router import api_router
from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description=(
        "Provenance-Reasoned Intelligent Synthesis "
        "for Multi-channel Content"
    ),
    version="0.1.0",
)

app.include_router(api_router)
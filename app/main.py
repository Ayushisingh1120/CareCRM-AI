from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging

from app.api.routes.health import router as health_router
from app.api.routes.chat import router as chat_router


setup_logging()


app = FastAPI(
    title=settings.app_name,
    description="AI-powered customer support copilot",
    version="0.1.0"
)


app.include_router(health_router)
app.include_router(chat_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to CareCRM AI",
        "version": "0.1.0"
    }
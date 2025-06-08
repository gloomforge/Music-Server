from fastapi import FastAPI

from .config import settings
from .events import register_shutdown, register_startup
from .routes import include_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.RECOD_URL,
    )

    register_startup(app)
    register_shutdown(app)

    include_routes(app)

    @app.get("/health")
    async def health_check():
        return {"message": "ok"}

    return app

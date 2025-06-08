from fastapi import FastAPI

from src.db.engine import db_close, db_init


def register_startup(app: FastAPI) -> None:
    @app.on_event("startup")
    async def on_startup():
        await db_init()


def register_shutdown(app: FastAPI) -> None:
    @app.on_event("shutdown")
    async def on_shutdown():
        await db_close()

from fastapi import FastAPI

from src.albums.routes import router as albums_router
from src.artists.routes import router as artists_router
from src.auth.routes import router as auth_router
from src.genres.routes import router as genres_router
from src.media_files.routes import router as media_files_router
from src.tracks.routes import router as tracks_router
from src.users.routes import router as users_router

prefix = "/api"


def include_routes(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/api")
    app.include_router(users_router, prefix="/api")
    app.include_router(genres_router, prefix="/api")
    app.include_router(artists_router, prefix="/api")
    app.include_router(albums_router, prefix="/api")
    app.include_router(tracks_router, prefix="/api")
    app.include_router(media_files_router, prefix="/api")

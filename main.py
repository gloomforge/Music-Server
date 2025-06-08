import uvicorn

from app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

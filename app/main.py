from fastapi import FastAPI

app = FastAPI(
    title="Task Manager",
    description="A simple Task Manager API with CRUD operations",
    version="1.0.0",
)

from .routes import router

app.include_router(router)

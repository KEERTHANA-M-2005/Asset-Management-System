from fastapi import FastAPI
from .database import engine
from . import models
from .routers import employees, assets

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AssetTrack Pro API",
    description="Backend API for AssetTrack Pro",
    version="1.0.0"
)

app.include_router(employees.router)
app.include_router(assets.router)
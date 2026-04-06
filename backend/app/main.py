from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
import app.models  # ✅ ONLY THIS IMPORT (NO routers inside models)

from app.routers import employees, assets, assignments, reports


# ✅ Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AssetTrack Pro API",
    version="1.0.0"
)


# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Routes
app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "Backend running 🚀"}
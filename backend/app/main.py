from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine, Base, SessionLocal
import app.models as models

from app.routers import employees, assets, assignments, reports
from app.routers import auth as auth_router


# ── Create / migrate tables ───────────────────────────────────────────────────

Base.metadata.create_all(bind=engine)

# Add columns introduced by auth that may not exist in the existing SQLite DB.
# SQLite does not support IF NOT EXISTS in ALTER TABLE, so we catch the error.
_MIGRATIONS = [
    "ALTER TABLE users ADD COLUMN email TEXT",
    "ALTER TABLE users ADD COLUMN employee_id INTEGER REFERENCES employees(employee_id)",
]

with engine.connect() as _conn:
    for _stmt in _MIGRATIONS:
        try:
            _conn.execute(text(_stmt))
            _conn.commit()
        except Exception:
            pass  # column already exists


# ── Seed roles (required for signup to work) ─────────────────────────────────

def _seed_roles() -> None:
    db = SessionLocal()
    try:
        if not db.query(models.Role).filter_by(role_name="admin").first():
            db.add(models.Role(role_name="admin", permissions="all"))
            db.commit()
        if not db.query(models.Role).filter_by(role_name="employee").first():
            db.add(models.Role(role_name="employee", permissions="read:own"))
            db.commit()
    finally:
        db.close()


_seed_roles()


# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(title="AssetTrack Pro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "AssetTrack Pro API running"}

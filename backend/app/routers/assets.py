from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(
    prefix="/api/assets",
    tags=["Assets"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.AssetResponse)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    """
    Create a new asset.
    """
    new_asset = models.Asset(**asset.dict())
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset


@router.get("/", response_model=list[schemas.AssetResponse])
def get_assets(db: Session = Depends(get_db)):
    """
    Retrieve all assets.
    """
    return db.query(models.Asset).all()
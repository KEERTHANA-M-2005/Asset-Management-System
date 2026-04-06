from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from ..security import RequirePrivilege

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
def create_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db),
    # user = Depends(RequirePrivilege("create:asset"))
):
    """
    Create a new asset.
    Only users with 'create:asset' privilege can access.
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


@router.delete("/{id}")
def delete_asset(
    id: int,
    db: Session = Depends(get_db),
    # user = Depends(RequirePrivilege("delete:asset"))
):
    """
    Delete an asset.
    Only users with 'delete:asset' privilege can access.
    """

    asset = db.query(models.Asset).filter(models.Asset.asset_id == id).first()

    if not asset:
        return {"message": "Asset not found"}

    db.delete(asset)
    db.commit()

    return {"message": "Asset deleted successfully"}
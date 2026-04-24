from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..security import get_db, get_current_user, require_role

router = APIRouter(prefix="/api/assets", tags=["Assets"])


@router.post("/", response_model=schemas.AssetResponse)
def create_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_role("admin")),
):
    new_asset = models.Asset(**asset.dict())
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset


@router.get("/", response_model=list[schemas.AssetResponse])
def get_assets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role.role_name.lower() == "admin":
        return db.query(models.Asset).all()

    # Employee: only assets currently assigned to them
    assigned_ids = [
        row[0]
        for row in db.query(models.Assignment.asset_id)
        .filter(
            models.Assignment.employee_id == current_user.employee_id,
            models.Assignment.status == "ASSIGNED",
        )
        .all()
    ]
    return db.query(models.Asset).filter(models.Asset.asset_id.in_(assigned_ids)).all()


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_role("admin")),
):
    asset = db.query(models.Asset).filter(models.Asset.asset_id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(asset)
    db.commit()
    return {"message": "Asset deleted successfully"}

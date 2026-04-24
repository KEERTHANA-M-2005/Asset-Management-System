from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from .. import models, schemas
from ..security import get_db, get_current_user, require_role

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])


@router.post("/", response_model=schemas.AssignmentResponse)
def create_assignment(
    assignment: schemas.AssignmentCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_role("admin")),
):
    asset = db.query(models.Asset).filter(models.Asset.asset_id == assignment.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.asset_status != "AVAILABLE":
        raise HTTPException(status_code=400, detail="Asset is not available for assignment")

    employee = db.query(models.Employee).filter(models.Employee.employee_id == assignment.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = db.query(models.Assignment).filter(
        models.Assignment.asset_id == assignment.asset_id,
        models.Assignment.status == "ASSIGNED",
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Asset is already assigned")

    new_assignment = models.Assignment(
        asset_id=assignment.asset_id,
        employee_id=assignment.employee_id,
        assigned_date=datetime.utcnow(),
        status="ASSIGNED",
    )
    asset.asset_status = "ASSIGNED"
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment


@router.get("/", response_model=list[schemas.AssignmentResponse])
def get_assignments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role.role_name.lower() == "admin":
        return db.query(models.Assignment).all()

    # Employee sees only their own assignments
    return (
        db.query(models.Assignment)
        .filter(models.Assignment.employee_id == current_user.employee_id)
        .all()
    )


@router.put("/{assignment_id}/return", response_model=schemas.AssignmentResponse)
def return_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_role("admin")),
):
    assignment = db.query(models.Assignment).filter(
        models.Assignment.assignment_id == assignment_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if assignment.status == "RETURNED":
        raise HTTPException(status_code=400, detail="Assignment already returned")

    assignment.returned_date = datetime.utcnow()
    assignment.status = "RETURNED"

    asset = db.query(models.Asset).filter(models.Asset.asset_id == assignment.asset_id).first()
    if asset:
        asset.asset_status = "AVAILABLE"

    db.commit()
    db.refresh(assignment)
    return assignment


@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_role("admin")),
):
    assignment = db.query(models.Assignment).filter(
        models.Assignment.assignment_id == assignment_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Free the asset if it was still assigned
    if assignment.status == "ASSIGNED":
        asset = db.query(models.Asset).filter(models.Asset.asset_id == assignment.asset_id).first()
        if asset:
            asset.asset_status = "AVAILABLE"

    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}

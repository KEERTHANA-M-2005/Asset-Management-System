from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(
    prefix="/api/assignments",
    tags=["Assignments"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.AssignmentResponse)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    """
    Assign an asset to an employee.
    """
    # Check if asset exists and is available
    asset = db.query(models.Asset).filter(models.Asset.asset_id == assignment.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.asset_status != "AVAILABLE":
        raise HTTPException(status_code=400, detail="Asset is not available for assignment")

    # Check if employee exists
    employee = db.query(models.Employee).filter(models.Employee.employee_id == assignment.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if asset is already assigned to someone else
    existing_assignment = db.query(models.Assignment).filter(
        models.Assignment.asset_id == assignment.asset_id,
        models.Assignment.status == "ASSIGNED"
    ).first()
    if existing_assignment:
        raise HTTPException(status_code=400, detail="Asset is already assigned")

    # Create assignment
    new_assignment = models.Assignment(
        asset_id=assignment.asset_id,
        employee_id=assignment.employee_id,
        assigned_date=datetime.utcnow(),
        status="ASSIGNED"
    )

    # Update asset status
    asset.asset_status = "ASSIGNED"

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment


@router.get("/", response_model=list[schemas.AssignmentResponse])
def get_assignments(db: Session = Depends(get_db)):
    """
    Retrieve all assignments with asset and employee details.
    """
    return db.query(models.Assignment).all()


@router.put("/{assignment_id}/return", response_model=schemas.AssignmentResponse)
def return_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """
    Mark an assignment as returned.
    """
    assignment = db.query(models.Assignment).filter(models.Assignment.assignment_id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment.status == "RETURNED":
        raise HTTPException(status_code=400, detail="Assignment is already returned")

    # Update assignment
    assignment.returned_date = datetime.utcnow()
    assignment.status = "RETURNED"

    # Update asset status back to available
    asset = db.query(models.Asset).filter(models.Asset.asset_id == assignment.asset_id).first()
    if asset:
        asset.asset_status = "AVAILABLE"

    db.commit()
    db.refresh(assignment)

    return assignment
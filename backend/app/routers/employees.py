from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..security import get_db, require_role, hash_password

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.post("/", response_model=schemas.EmployeeResponse, status_code=201)
def create_employee(
    data: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_role("admin")),
):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    new_employee = models.Employee(
        employee_name=data.employee_name,
        department=data.department,
    )
    db.add(new_employee)
    db.flush()

    emp_role = db.query(models.Role).filter(models.Role.role_name == "employee").first()
    if not emp_role:
        raise HTTPException(status_code=500, detail="Employee role not configured")

    new_user = models.User(
        username=data.email,
        email=data.email,
        password=hash_password(data.password),
        role_id=emp_role.role_id,
        employee_id=new_employee.employee_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_employee)
    db.refresh(new_user)

    return {
        "employee_id": new_employee.employee_id,
        "employee_name": new_employee.employee_name,
        "department": new_employee.department,
        "email": new_user.email,
        "user_id": new_user.user_id,
    }


@router.get("/", response_model=List[schemas.EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_role("admin")),
):
    employees = db.query(models.Employee).all()
    result = []
    for emp in employees:
        user = db.query(models.User).filter(models.User.employee_id == emp.employee_id).first()
        result.append({
            "employee_id": emp.employee_id,
            "employee_name": emp.employee_name,
            "department": emp.department,
            "email": user.email if user else None,
            "user_id": user.user_id if user else None,
        })
    return result


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_role("admin")),
):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    user = db.query(models.User).filter(models.User.employee_id == employee_id).first()
    if user:
        db.delete(user)

    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..security import verify_password, create_access_token, hash_password, get_db
from .. import models, schemas

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.TokenResponse)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token({
        "sub": str(user.user_id),
        "role": user.role.role_name,
        "email": user.email,
        "employee_id": user.employee_id,
    })

    return schemas.TokenResponse(
        access_token=token,
        role=user.role.role_name,
        user_id=user.user_id,
        email=user.email,
        employee_id=user.employee_id,
    )


@router.post("/signup", response_model=schemas.TokenResponse, status_code=201)
def signup(data: schemas.SignupRequest, db: Session = Depends(get_db)):
    role_name = data.role.lower()
    if role_name not in ("admin", "employee"):
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'employee'")

    if role_name == "employee" and not data.department:
        raise HTTPException(status_code=400, detail="Department is required for employee accounts")

    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    role = db.query(models.Role).filter(models.Role.role_name == role_name).first()
    if not role:
        raise HTTPException(status_code=500, detail=f"Role '{role_name}' not configured. Contact support.")

    employee_id = None
    if role_name == "employee":
        new_employee = models.Employee(
            employee_name=data.full_name,
            department=data.department,
        )
        db.add(new_employee)
        db.flush()
        employee_id = new_employee.employee_id

    new_user = models.User(
        username=data.email,
        email=data.email,
        password=hash_password(data.password),
        role_id=role.role_id,
        employee_id=employee_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({
        "sub": str(new_user.user_id),
        "role": role.role_name,
        "email": new_user.email,
        "employee_id": new_user.employee_id,
    })

    return schemas.TokenResponse(
        access_token=token,
        role=role.role_name,
        user_id=new_user.user_id,
        email=new_user.email,
        employee_id=new_user.employee_id,
    )

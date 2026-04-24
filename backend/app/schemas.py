from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: str          # "admin" or "employee"
    department: Optional[str] = None  # required when role == "employee"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    email: str
    employee_id: Optional[int] = None


# ── Employee ──────────────────────────────────────────────────────────────────

class EmployeeCreate(BaseModel):
    employee_name: str
    department: str
    email: str
    password: str


class EmployeeResponse(BaseModel):
    employee_id: int
    employee_name: str
    department: str
    email: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


# ── Asset ─────────────────────────────────────────────────────────────────────

class AssetCreate(BaseModel):
    asset_name: str


class AssetResponse(BaseModel):
    asset_id: int
    asset_name: str
    asset_status: str

    class Config:
        from_attributes = True


# ── Assignment ────────────────────────────────────────────────────────────────

class AssignmentCreate(BaseModel):
    asset_id: int
    employee_id: int


class AssignmentResponse(BaseModel):
    assignment_id: int
    asset_id: int
    employee_id: int
    assigned_date: datetime
    returned_date: Optional[datetime] = None
    status: str
    asset: Optional[AssetResponse] = None
    employee: Optional[EmployeeResponse] = None

    class Config:
        from_attributes = True


class AssignmentReturn(BaseModel):
    returned_date: datetime

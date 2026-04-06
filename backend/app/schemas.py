from pydantic import BaseModel
from datetime import datetime


# Employee Schemas
class EmployeeCreate(BaseModel):
    employee_name: str
    department: str


class EmployeeResponse(BaseModel):
    employee_id: int
    employee_name: str
    department: str

    class Config:
        from_attributes = True


# Asset Schemas
class AssetCreate(BaseModel):
    asset_name: str


class AssetResponse(BaseModel):
    asset_id: int
    asset_name: str
    asset_status: str

    class Config:
        from_attributes = True


# Assignment Schemas
class AssignmentCreate(BaseModel):
    asset_id: int
    employee_id: int


class AssignmentResponse(BaseModel):
    assignment_id: int
    asset_id: int
    employee_id: int
    assigned_date: datetime
    returned_date: datetime | None
    status: str
    asset: AssetResponse | None
    employee: EmployeeResponse | None

    class Config:
        from_attributes = True


class AssignmentReturn(BaseModel):
    returned_date: datetime
        
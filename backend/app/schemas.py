from pydantic import BaseModel


# Employee Schemas
class EmployeeCreate(BaseModel):
    employee_name: str
    department: str


class EmployeeResponse(BaseModel):
    employee_id: int
    employee_name: str
    department: str

    class Config:
        orm_mode = True


# Asset Schemas
class AssetCreate(BaseModel):
    asset_name: str


class AssetResponse(BaseModel):
    asset_id: int
    asset_name: str
    asset_status: str

    class Config:
        orm_mode = True
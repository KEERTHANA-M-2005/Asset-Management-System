from sqlalchemy import Column, Integer, String
from .database import Base


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    department = Column(String, nullable=False)


class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String, nullable=False)
    asset_status = Column(String, default="AVAILABLE")
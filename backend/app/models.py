from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True)
    permissions = Column(String)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

    role_id = Column(Integer, ForeignKey("roles.role_id"))
    role = relationship("Role")


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


class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    assigned_date = Column(DateTime, nullable=False)
    returned_date = Column(DateTime, nullable=True)
    status = Column(String, default="ASSIGNED")  # ASSIGNED or RETURNED

    # Relationships
    asset = relationship("Asset")
    employee = relationship("Employee")
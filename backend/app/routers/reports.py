from collections import Counter
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_reports(period: str = "30d", db: Session = Depends(get_db)):
    now = datetime.utcnow()
    period_map = {
        "7d": 7,
        "30d": 30,
        "90d": 90,
        "1y": 365,
    }
    days = period_map.get(period, 30)
    cutoff = now - timedelta(days=days)

    assets = db.query(models.Asset).all()
    employees = db.query(models.Employee).all()
    assignments = db.query(models.Assignment).all()

    total_assets = len(assets)
    total_employees = len(employees)
    active_assignments = sum(1 for assignment in assignments if assignment.status == "ASSIGNED")
    available_assets = sum(1 for asset in assets if asset.asset_status == "AVAILABLE")
    overdue_returns = sum(
        1
        for assignment in assignments
        if assignment.status == "ASSIGNED" and assignment.assigned_date < cutoff
    )

    status_counts = Counter((asset.asset_status or "UNKNOWN").upper() for asset in assets)
    asset_status_distribution = []
    for status, count in status_counts.items():
        percentage = round((count / total_assets) * 100, 2) if total_assets else 0.0
        asset_status_distribution.append({
            "status": status.title(),
            "count": count,
            "percentage": percentage,
        })

    department_counts = Counter()
    for assignment in assignments:
        if assignment.employee and assignment.employee.department:
            department_counts[assignment.employee.department] += 1

    department_usage = []
    for department, count in department_counts.items():
        percentage = round((count / total_assets) * 100, 2) if total_assets else 0.0
        department_usage.append({
            "department": department,
            "assetCount": count,
            "percentage": percentage,
        })

    recent_activity = []
    for assignment in assignments:
        if assignment.assigned_date:
            recent_activity.append({
                "description": f"{assignment.employee.employee_name if assignment.employee else 'Unknown employee'} assigned {assignment.asset.asset_name if assignment.asset else 'Unknown asset'}",
                "timestamp": assignment.assigned_date.isoformat(),
            })
        if assignment.returned_date:
            recent_activity.append({
                "description": f"{assignment.employee.employee_name if assignment.employee else 'Unknown employee'} returned {assignment.asset.asset_name if assignment.asset else 'Unknown asset'}",
                "timestamp": assignment.returned_date.isoformat(),
            })

    recent_activity.sort(key=lambda item: item["timestamp"], reverse=True)
    recent_activity = recent_activity[:5]

    asset_type_counts = Counter((getattr(asset, "asset_type", None) or "Unknown").title() for asset in assets)
    asset_types = [
        {
            "type": asset_type,
            "count": count,
            "percentage": round((count / total_assets) * 100, 2) if total_assets else 0.0,
        }
        for asset_type, count in asset_type_counts.items()
    ]

    return {
        "totalAssets": total_assets,
        "activeAssignments": active_assignments,
        "availableAssets": available_assets,
        "overdueReturns": overdue_returns,
        "assetStatusDistribution": asset_status_distribution,
        "departmentUsage": department_usage,
        "recentActivity": recent_activity,
        "assetTypes": asset_types,
    }

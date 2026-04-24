from collections import Counter
from datetime import datetime, timedelta
import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from .. import models
from ..security import get_db, get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])


def _build_report_data(assignments, assets, is_admin: bool, period: str):
    now = datetime.utcnow()
    days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
    cutoff = now - timedelta(days=days)

    total_assets = len(assets)
    active_assignments = sum(1 for a in assignments if a.status == "ASSIGNED")
    available_assets = sum(1 for a in assets if a.asset_status == "AVAILABLE")
    overdue_returns = sum(
        1 for a in assignments
        if a.status == "ASSIGNED" and a.assigned_date < cutoff
    )

    status_counts = Counter((a.asset_status or "UNKNOWN").upper() for a in assets)
    asset_status_distribution = [
        {
            "status": s.title(),
            "count": c,
            "percentage": round((c / total_assets) * 100, 2) if total_assets else 0.0,
        }
        for s, c in status_counts.items()
    ]

    dept_counts: Counter = Counter()
    for a in assignments:
        if a.employee and a.employee.department:
            dept_counts[a.employee.department] += 1

    department_usage = [
        {
            "department": dept,
            "assetCount": count,
            "percentage": round((count / total_assets) * 100, 2) if total_assets else 0.0,
        }
        for dept, count in dept_counts.items()
    ] if is_admin else []

    recent_activity = []
    for a in assignments:
        emp_name = a.employee.employee_name if a.employee else "Unknown"
        asset_name = a.asset.asset_name if a.asset else "Unknown"
        if a.assigned_date:
            recent_activity.append({
                "description": f"{emp_name} was assigned {asset_name}",
                "timestamp": a.assigned_date.isoformat(),
            })
        if a.returned_date:
            recent_activity.append({
                "description": f"{emp_name} returned {asset_name}",
                "timestamp": a.returned_date.isoformat(),
            })

    recent_activity.sort(key=lambda x: x["timestamp"], reverse=True)
    recent_activity = recent_activity[:10]

    type_counts = Counter((getattr(a, "asset_type", None) or "General").title() for a in assets)
    asset_types = [
        {
            "type": t,
            "count": c,
            "percentage": round((c / total_assets) * 100, 2) if total_assets else 0.0,
        }
        for t, c in type_counts.items()
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


@router.get("/")
def get_reports(
    period: str = "30d",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    is_admin = current_user.role.role_name.lower() == "admin"

    if is_admin:
        assets = db.query(models.Asset).all()
        assignments = db.query(models.Assignment).all()
    else:
        assignments = db.query(models.Assignment).filter(
            models.Assignment.employee_id == current_user.employee_id
        ).all()
        asset_ids = [a.asset_id for a in assignments]
        assets = db.query(models.Asset).filter(models.Asset.asset_id.in_(asset_ids)).all()

    return _build_report_data(assignments, assets, is_admin, period)


@router.get("/download")
def download_report(
    period: str = "30d",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    is_admin = current_user.role.role_name.lower() == "admin"
    now = datetime.utcnow()

    if is_admin:
        assignments = db.query(models.Assignment).all()
    else:
        assignments = db.query(models.Assignment).filter(
            models.Assignment.employee_id == current_user.employee_id
        ).all()

    output = io.StringIO()
    writer = csv.writer(output)

    if is_admin:
        writer.writerow(["Assignment ID", "Employee Name", "Department", "Asset Name", "Status", "Assigned Date", "Returned Date"])
        for a in assignments:
            writer.writerow([
                a.assignment_id,
                a.employee.employee_name if a.employee else "Unknown",
                a.employee.department if a.employee else "Unknown",
                a.asset.asset_name if a.asset else "Unknown",
                a.status,
                a.assigned_date.strftime("%Y-%m-%d") if a.assigned_date else "",
                a.returned_date.strftime("%Y-%m-%d") if a.returned_date else "",
            ])
    else:
        writer.writerow(["Assignment ID", "Asset Name", "Status", "Assigned Date", "Returned Date"])
        for a in assignments:
            writer.writerow([
                a.assignment_id,
                a.asset.asset_name if a.asset else "Unknown",
                a.status,
                a.assigned_date.strftime("%Y-%m-%d") if a.assigned_date else "",
                a.returned_date.strftime("%Y-%m-%d") if a.returned_date else "",
            ])

    output.seek(0)
    filename = f"assettrack_report_{period}_{now.strftime('%Y%m%d')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

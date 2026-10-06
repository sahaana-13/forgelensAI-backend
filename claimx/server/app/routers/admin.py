from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import require_role
from app.models.accident import Accident
from app.models.evidence import Evidence
from app.models.fnol import FnolReport
from app.models.analysis import StatementComparison, MissingInformation
router=APIRouter(prefix="/api/admin",tags=["Admin"])
@router.get("/dashboard")
def dashboard(user=Depends(require_role("ADMIN")),db:Session=Depends(get_db)):
    incidents=db.query(Accident).all(); return {"total_incidents":len(incidents),"active_incidents":sum(a.status not in {"COMPLETED","CANCELLED"} for a in incidents),"completed_fnols":db.query(FnolReport).count(),"pending_review":sum(a.status in {"FNOL_DRAFT","UNDER_REVIEW"} for a in incidents),"missing_information":db.query(MissingInformation).filter_by(status="MISSING").count(),"conflicting_statements":sum(1 for c in db.query(StatementComparison).all() if any(i.get("status")=="CONFLICTING" for i in c.result.get("items",[])))}
@router.get("/accidents")
def accidents(user=Depends(require_role("ADMIN")),db:Session=Depends(get_db)): return db.query(Accident).order_by(Accident.id.desc()).all()
@router.get("/reports")
def reports(user=Depends(require_role("ADMIN")),db:Session=Depends(get_db)): return db.query(FnolReport).order_by(FnolReport.id.desc()).all()

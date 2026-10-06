import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.accident import Accident
from app.models.fnol import FnolReport
from app.models.user import UserProfile
from app.models.vehicle import Vehicle
from app.models.insurance import InsurancePolicy
from app.models.interview import Statement
from app.models.evidence import Evidence
from app.models.analysis import MissingInformation, StatementComparison
from app.services.fnol_service import build_fnol_data
from app.services.pdf_service import build_pdf
router=APIRouter(prefix="/api/accidents",tags=["FNOL"])
def check(a,user):
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
@router.post("/{id}/fnol")
async def generate(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id); check(a,user)
    profile=db.get(UserProfile,a.claimant_id); vehicle=db.get(Vehicle,a.vehicle_id) if a.vehicle_id else None; policies=db.query(InsurancePolicy).filter_by(owner_id=a.claimant_id).all(); statements=db.query(Statement).filter_by(accident_id=id).all(); evidence=db.query(Evidence).filter_by(accident_id=id).all(); missing=db.query(MissingInformation).filter_by(accident_id=id).all(); comparison=db.query(StatementComparison).filter_by(accident_id=id).order_by(StatementComparison.id.desc()).first()
    data=await build_fnol_data(a,statements,evidence,missing,policies,profile,vehicle,comparison.result if comparison else None)
    content=json.dumps(data,indent=2)
    row=db.query(FnolReport).filter_by(accident_id=id).first()
    now=datetime.now(timezone.utc).replace(tzinfo=None)
    if row: row.content=content; row.updated_at=now
    else: row=FnolReport(accident_id=id,content=content,generated_at=now,updated_at=now); db.add(row)
    a.status="FNOL_DRAFT"; db.commit(); return data
@router.get("/{id}/fnol")
def get_fnol(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id); check(a,user); row=db.query(FnolReport).filter_by(accident_id=id).first(); return json.loads(row.content) if row else None
@router.put("/{id}/fnol")
def update_fnol(id:int,payload:dict,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id); check(a,user); row=db.query(FnolReport).filter_by(accident_id=id).first()
    if not row: raise HTTPException(404,"FNOL not generated")
    row.content=json.dumps(payload,indent=2); row.updated_at=datetime.now(timezone.utc).replace(tzinfo=None); db.commit(); return payload
@router.get("/{id}/fnol/pdf")
def pdf(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id); check(a,user); row=db.query(FnolReport).filter_by(accident_id=id).first()
    if not row: raise HTTPException(404,"FNOL not generated")
    data=json.loads(row.content); sections=[]
    for k,v in data.items(): sections.append((k.replace('_',' ').title(), json.dumps(v,indent=2) if isinstance(v,(dict,list)) else str(v)))
    buf=build_pdf(f"FIRST NOTICE OF LOSS — {a.incident_id}",sections)
    return StreamingResponse(buf,media_type="application/pdf",headers={"Content-Disposition":f'attachment; filename="{a.incident_id}-FNOL.pdf"'})

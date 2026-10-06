from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.accident import Accident
from app.models.interview import Statement
from app.models.analysis import StatementComparison, EvidenceAnalysis, MissingInformation
from app.models.evidence import Evidence
from app.services.comparison_service import run_comparison
router=APIRouter(prefix="/api/accidents",tags=["Analysis"])
def check(a,user):
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
@router.post("/{id}/compare-statements")
async def compare(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id); check(a,user); rows=db.query(Statement).filter_by(accident_id=id).all()
    row=await run_comparison(db,id,rows); a.status="ANALYSIS_COMPLETED"; db.commit(); return row.result
@router.get("/{id}/comparison")
def get_compare(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id); check(a,user); row=db.query(StatementComparison).filter_by(accident_id=id).order_by(StatementComparison.id.desc()).first(); return row.result if row else {"items":[]}
@router.post("/{id}/analyze-evidence")
def evidence_analysis(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id); check(a,user); evidence=db.query(Evidence).filter_by(accident_id=id).all(); statements=db.query(Statement).filter_by(accident_id=id).all()
    results=[]
    for s in statements:
        results.append({"source":f"Party {s.party_label}","status":"UNVERIFIED","detail":"Statement is user-reported; available evidence does not independently establish the claim."})
    if a.accident_time and evidence: results.append({"source":"Accident timestamp","status":"SUPPORTED","detail":"Evidence was uploaded after the recorded accident time; this does not independently establish causation."})
    result={"items":results}; row=EvidenceAnalysis(accident_id=id,result=result,created_at=datetime.now(timezone.utc).replace(tzinfo=None)); db.add(row); db.commit(); return result
@router.get("/{id}/evidence-analysis")
def get_evidence_analysis(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id); check(a,user); row=db.query(EvidenceAnalysis).filter_by(accident_id=id).order_by(EvidenceAnalysis.id.desc()).first(); return row.result if row else {"items":[]}
@router.get("/{id}/missing-information")
def missing(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id); check(a,user); existing=db.query(MissingInformation).filter_by(accident_id=id).all()
    if not existing:
        statements=db.query(Statement).filter_by(accident_id=id).all(); evidence=db.query(Evidence).filter_by(accident_id=id).all()
        items=[]
        if not a.vehicle_id: items.append(("Vehicle information","No vehicle is linked to this incident"))
        if not evidence: items.append(("Accident photograph","No evidence has been uploaded"))
        if not any(s.party_label=="A" for s in statements): items.append(("Party A statement","Party A interview/statement is missing"))
        if not any(s.party_label=="B" for s in statements): items.append(("Party B statement","Party B interview/statement is missing"))
        for item,reason in items: db.add(MissingInformation(accident_id=id,item=item,reason=reason,created_at=datetime.now(timezone.utc).replace(tzinfo=None)))
        db.commit(); existing=db.query(MissingInformation).filter_by(accident_id=id).all()
    return existing

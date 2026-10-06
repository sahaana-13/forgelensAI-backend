from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.accident import Accident, AccidentParty
from app.models.notification import Notification
from app.schemas.accident import AccidentCreate, AccidentOut, PartyIn, ClaimTypeIn
from app.services.accident_service import next_incident_id
router=APIRouter(prefix="/api/accidents",tags=["Accidents"])
@router.get("",response_model=list[AccidentOut])
def list_accidents(user=Depends(get_current_user),db:Session=Depends(get_db)):
    q=db.query(Accident)
    return q.filter(Accident.claimant_id==user.id).order_by(Accident.id.desc()).all() if user.role=="CLAIMANT" else q.order_by(Accident.id.desc()).all()
@router.post("",response_model=AccidentOut)
def create(data:AccidentCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=Accident(incident_id=next_incident_id(db),claimant_id=user.id,accident_time=data.accident_time or datetime.now(timezone.utc).replace(tzinfo=None),**data.model_dump(exclude={"accident_time"})); db.add(a); db.commit(); db.refresh(a); return a
@router.post("/sos",response_model=AccidentOut)
def sos(data:AccidentCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=Accident(incident_id=next_incident_id(db),claimant_id=user.id,accident_time=data.accident_time or datetime.now(timezone.utc).replace(tzinfo=None),status="EVIDENCE_COLLECTION",**data.model_dump(exclude={"accident_time"})); db.add(a); db.flush(); db.add(Notification(user_id=user.id,message=f"Accident incident {a.incident_id} has been created.",created_at=datetime.now(timezone.utc).replace(tzinfo=None))); db.commit(); db.refresh(a); return a
@router.get("/{id}",response_model=AccidentOut)
def get(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id)
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
    return a
@router.put("/{id}",response_model=AccidentOut)
def update(id:int,data:AccidentCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id)
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(a,k,v)
    db.commit(); db.refresh(a); return a
@router.post("/{id}/parties")
def add_party(id:int,data:PartyIn,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id)
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
    p=AccidentParty(accident_id=id,**data.model_dump()); db.add(p); db.commit(); db.refresh(p); return p
@router.patch("/{id}/claim-type")
def set_claim_type(id:int,data:ClaimTypeIn,user=Depends(get_current_user),db:Session=Depends(get_db)):
    if data.claim_type not in {"Own Damage","Third Party","Both"}: raise HTTPException(400,"Invalid claim type")
    a=db.get(Accident,id)
    if not a or a.claimant_id!=user.id: raise HTTPException(404,"Accident not found")
    a.claim_type=data.claim_type; db.commit(); return {"claim_type":a.claim_type}

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.accident import Accident
from app.models.evidence import Evidence
from app.services.evidence_service import save_upload
import uuid
router=APIRouter(prefix="/api",tags=["Evidence"])
@router.get("/accidents/{id}/evidence")
def list_evidence(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id)
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
    return db.query(Evidence).filter_by(accident_id=id).order_by(Evidence.id.desc()).all()
@router.post("/accidents/{id}/evidence")
async def upload(id:int,file:UploadFile=File(...),evidence_type:str=Form("ACCIDENT_PHOTO"),description:str=Form(""),latitude:float|None=Form(None),longitude:float|None=Form(None),user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id)
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
    stored,path=await save_upload(file)
    e=Evidence(evidence_id=f"EVD-{uuid.uuid4().hex[:8].upper()}",accident_id=id,evidence_type=evidence_type,file_name=file.filename or stored,file_path=path,uploaded_by=user.id,uploaded_at=datetime.now(timezone.utc).replace(tzinfo=None),latitude=latitude,longitude=longitude,description=description,status="UNVERIFIED"); db.add(e); db.commit(); db.refresh(e); return e
@router.delete("/evidence/{id}")
def delete(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    e=db.get(Evidence,id)
    if not e: raise HTTPException(404,"Evidence not found")
    a=db.get(Accident,e.accident_id)
    if user.role=="CLAIMANT" and a.claimant_id!=user.id: raise HTTPException(403,"Forbidden")
    db.delete(e); db.commit(); return {"ok":True}

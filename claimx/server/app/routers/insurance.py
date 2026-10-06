from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.insurance import InsurancePolicy
from app.schemas.insurance import InsuranceIn, InsuranceOut
router=APIRouter(prefix="/api/insurance",tags=["Insurance"])
@router.get("",response_model=list[InsuranceOut])
def list_policies(user=Depends(get_current_user),db:Session=Depends(get_db)): return db.query(InsurancePolicy).filter_by(owner_id=user.id).all()
@router.post("",response_model=InsuranceOut)
def add_policy(data:InsuranceIn,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=InsurancePolicy(owner_id=user.id,**data.model_dump()); db.add(p); db.commit(); db.refresh(p); return p
@router.put("/{id}",response_model=InsuranceOut)
def update_policy(id:int,data:InsuranceIn,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=db.query(InsurancePolicy).filter_by(id=id,owner_id=user.id).first()
    if not p: from fastapi import HTTPException; raise HTTPException(404,"Policy not found")
    for k,v in data.model_dump().items(): setattr(p,k,v)
    db.commit(); db.refresh(p); return p

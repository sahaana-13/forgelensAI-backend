from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.accident import Accident
from app.models.interview import Statement
from app.schemas.accident import PartyIn
from app.services.statement_service import save_statement
router=APIRouter(prefix="/api",tags=["Statements"])
@router.get("/accidents/{id}/statements")
def statements(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,id)
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
    return db.query(Statement).filter_by(accident_id=id).all()
@router.post("/statements")
async def create_statement(payload:dict,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,payload.get("accident_id"))
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
    if payload.get("party_label") not in {"A","B"}: raise HTTPException(400,"Invalid party")
    return await save_statement(db,a.id,payload["party_label"],payload.get("raw_text", ""))

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.accident import Accident
from app.models.interview import Interview, InterviewMessage
from app.schemas.interview import InterviewStart, MessageIn
from app.services.gemini_service import interview_reply
router=APIRouter(prefix="/api/interviews",tags=["AI Interviews"])
@router.post("/start")
async def start(data:InterviewStart,user=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(Accident,data.accident_id)
    if not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Accident not found")
    if data.party_label not in {"A","B"}: raise HTTPException(400,"Party must be A or B")
    interview=Interview(accident_id=a.id,party_label=data.party_label,started_at=datetime.now(timezone.utc).replace(tzinfo=None)); db.add(interview); db.flush()
    opening="Please describe what happened immediately before the accident."
    msg=InterviewMessage(interview_id=interview.id,sender="AI",message=opening,created_at=datetime.now(timezone.utc).replace(tzinfo=None)); db.add(msg); db.commit(); db.refresh(interview)
    return {"id":interview.id,"party_label":interview.party_label,"message":opening}
@router.post("/{id}/message")
async def message(id:int,data:MessageIn,user=Depends(get_current_user),db:Session=Depends(get_db)):
    i=db.get(Interview,id); a=db.get(Accident,i.accident_id) if i else None
    if not i or not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Interview not found")
    history=[{"sender":m.sender,"message":m.message} for m in i.messages]
    db.add(InterviewMessage(interview_id=i.id,sender="USER",message=data.message,created_at=datetime.now(timezone.utc).replace(tzinfo=None))); db.commit()
    reply=await interview_reply(history,data.message,i.party_label)
    db.add(InterviewMessage(interview_id=i.id,sender="AI",message=reply,created_at=datetime.now(timezone.utc).replace(tzinfo=None))); db.commit()
    return {"reply":reply}
@router.get("/{id}")
def get_interview(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    i=db.get(Interview,id); a=db.get(Accident,i.accident_id) if i else None
    if not i or not a or (user.role=="CLAIMANT" and a.claimant_id!=user.id): raise HTTPException(404,"Interview not found")
    return {"id":i.id,"accident_id":i.accident_id,"party_label":i.party_label,"status":i.status,"messages":[{"sender":m.sender,"message":m.message,"created_at":m.created_at.isoformat()} for m in i.messages]}

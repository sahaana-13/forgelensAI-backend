from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.services.gemini_service import ask_gemini
router=APIRouter(prefix="/api/ai",tags=["AI"])
@router.post("/interview")
async def generic_interview(payload:dict,user=Depends(get_current_user)):
    return {"reply":await ask_gemini(payload.get("prompt",""))}

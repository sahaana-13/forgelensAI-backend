from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import UserProfile
from app.schemas.profile import ProfileIn, ProfileOut
router=APIRouter(prefix="/api/profile",tags=["Profile"])
@router.get("",response_model=ProfileOut)
def get_profile(user=Depends(get_current_user),db:Session=Depends(get_db)):
    if not user.profile: user.profile=UserProfile(user_id=user.id); db.commit(); db.refresh(user)
    return user.profile
@router.put("",response_model=ProfileOut)
def update_profile(data:ProfileIn,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=user.profile or UserProfile(user_id=user.id); db.add(p)
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(p,k,v)
    db.commit(); db.refresh(p); return p

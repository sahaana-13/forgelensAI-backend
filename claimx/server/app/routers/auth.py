from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User, UserProfile
from app.schemas.auth import RegisterIn, LoginIn, TokenOut, UserOut
from app.dependencies.auth import get_current_user
router=APIRouter(prefix="/api/auth",tags=["Auth"])
@router.post("/register",response_model=TokenOut)
def register(data:RegisterIn,db:Session=Depends(get_db)):
    if db.query(User).filter_by(email=data.email).first(): raise HTTPException(409,"Email already registered")
    role=data.role if data.role in {"CLAIMANT","ADMIN"} else "CLAIMANT"
    user=User(email=data.email,password_hash=hash_password(data.password),role=role,created_at=date.today()); db.add(user); db.flush(); db.add(UserProfile(user_id=user.id,full_name=data.full_name or None)); db.commit()
    return {"access_token":create_access_token(user.id,user.role),"token_type":"bearer"}
@router.post("/login",response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.query(User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    return {"access_token":create_access_token(user.id,user.role),"token_type":"bearer"}
@router.get("/me",response_model=UserOut)
def me(user=Depends(get_current_user)):
    return {"id":user.id,"email":user.email,"role":user.role,"full_name":user.profile.full_name if user.profile else None}

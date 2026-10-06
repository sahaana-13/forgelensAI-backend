from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.notification import Notification
router=APIRouter(prefix="/api/notifications",tags=["Notifications"])
@router.get("")
def list_notifications(user=Depends(get_current_user),db:Session=Depends(get_db)): return db.query(Notification).filter_by(user_id=user.id).order_by(Notification.id.desc()).all()
@router.patch("/{id}/read")
def mark_read(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    n=db.query(Notification).filter_by(id=id,user_id=user.id).first()
    if not n: raise HTTPException(404,"Notification not found")
    n.is_read=True; db.commit(); return {"ok":True}

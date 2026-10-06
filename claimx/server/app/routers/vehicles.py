from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleIn, VehicleOut
router=APIRouter(prefix="/api/vehicles",tags=["Vehicles"])
@router.get("",response_model=list[VehicleOut])
def list_vehicles(user=Depends(get_current_user),db:Session=Depends(get_db)): return db.query(Vehicle).filter_by(owner_id=user.id).all()
@router.post("",response_model=VehicleOut)
def add_vehicle(data:VehicleIn,user=Depends(get_current_user),db:Session=Depends(get_db)):
    v=Vehicle(owner_id=user.id,**data.model_dump()); db.add(v); db.commit(); db.refresh(v); return v
@router.get("/{id}",response_model=VehicleOut)
def get_vehicle(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    v=db.query(Vehicle).filter_by(id=id,owner_id=user.id).first()
    if not v: raise HTTPException(404,"Vehicle not found")
    return v
@router.put("/{id}",response_model=VehicleOut)
def update_vehicle(id:int,data:VehicleIn,user=Depends(get_current_user),db:Session=Depends(get_db)):
    v=db.query(Vehicle).filter_by(id=id,owner_id=user.id).first()
    if not v: raise HTTPException(404,"Vehicle not found")
    for k,vv in data.model_dump().items(): setattr(v,k,vv)
    db.commit(); db.refresh(v); return v

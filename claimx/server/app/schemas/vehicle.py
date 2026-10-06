from pydantic import BaseModel, Field
class VehicleIn(BaseModel):
    registration_number: str = Field(min_length=4, max_length=30)
    make: str
    model: str
    vehicle_type: str = "Car"
    manufacturing_year: int | None = None
    rc_number: str | None = None
class VehicleOut(VehicleIn):
    id: int
    owner_id: int
    class Config: from_attributes = True

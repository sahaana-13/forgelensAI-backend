from datetime import datetime
from pydantic import BaseModel
class AccidentCreate(BaseModel):
    vehicle_id: int | None = None
    accident_time: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_text: str | None = None
    description: str | None = None
    claim_type: str | None = None
class AccidentOut(BaseModel):
    id: int
    incident_id: str
    claimant_id: int
    vehicle_id: int | None
    accident_time: datetime
    latitude: float | None
    longitude: float | None
    location_text: str | None
    status: str
    claim_type: str | None
    description: str | None
    class Config: from_attributes = True
class PartyIn(BaseModel):
    party_label: str
    name: str | None = None
    contact: str | None = None
    vehicle_registration: str | None = None
class ClaimTypeIn(BaseModel):
    claim_type: str

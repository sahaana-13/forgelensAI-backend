from datetime import date
from pydantic import BaseModel
class ProfileIn(BaseModel):
    full_name: str | None = None
    date_of_birth: date | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    licence_number: str | None = None
    licence_type: str | None = None
    licence_issue_date: date | None = None
    licence_expiry_date: date | None = None
class ProfileOut(ProfileIn):
    id: int
    user_id: int
    class Config: from_attributes = True

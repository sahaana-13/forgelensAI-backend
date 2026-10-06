from datetime import date
from pydantic import BaseModel
class InsuranceIn(BaseModel):
    vehicle_id: int | None = None
    insurance_company: str
    policy_number: str
    start_date: date
    end_date: date
class InsuranceOut(InsuranceIn):
    id: int
    owner_id: int
    class Config: from_attributes = True

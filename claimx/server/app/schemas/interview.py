from pydantic import BaseModel
class InterviewStart(BaseModel):
    accident_id: int
    party_label: str
class MessageIn(BaseModel):
    message: str
class InterviewMessageOut(BaseModel):
    sender: str
    message: str
    created_at: str
class InterviewOut(BaseModel):
    id: int
    accident_id: int
    party_label: str
    status: str
    messages: list[InterviewMessageOut]

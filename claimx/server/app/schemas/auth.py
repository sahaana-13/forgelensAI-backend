from pydantic import BaseModel, EmailStr, Field
class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "CLAIMANT"
    full_name: str = ""
class LoginIn(BaseModel):
    email: EmailStr
    password: str
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
class UserOut(BaseModel):
    id: int
    email: str
    role: str
    full_name: str | None = None

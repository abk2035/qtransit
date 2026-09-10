from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 60 * 60


class UserMeResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    user_type: str
    company_id: int | None = None
    agency_id: int | None = None
    is_active: bool

    class Config:
        from_attributes = True

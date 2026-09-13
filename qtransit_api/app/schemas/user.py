from __future__ import annotations

from pydantic import BaseModel, EmailStr
from typing import List


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    company_id: int | None = None
    agency_id: int | None = None


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
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


class UsersListResponse(BaseModel):
    users: List[UserResponse]

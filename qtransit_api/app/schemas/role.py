from __future__ import annotations

from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    company_id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class RoleResponse(BaseModel):
    id: int
    company_id: int
    name: str
    description: str | None = None
    is_active: bool

    class Config:
        from_attributes = True

from __future__ import annotations

from pydantic import BaseModel, Field


class AgencyCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    code: str = Field(..., min_length=1, max_length=50)
    city: str | None = None
    country: str | None = None


class AgencyResponse(BaseModel):
    id: int
    company_id: int
    name: str
    code: str
    city: str | None = None
    country: str | None = None
    is_active: bool

    class Config:
        from_attributes = True

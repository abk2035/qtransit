from __future__ import annotations

from pydantic import BaseModel, Field


class PermissionCreate(BaseModel):
    company_id: int
    code: str = Field(..., min_length=1, max_length=120)
    name: str = Field(..., min_length=1, max_length=150)
    module_name: str = Field(..., min_length=1, max_length=80)
    action_name: str = Field(..., min_length=1, max_length=50)


class PermissionResponse(BaseModel):
    id: int
    company_id: int
    code: str
    name: str
    module_name: str
    action_name: str
    is_active: bool

    class Config:
        from_attributes = True

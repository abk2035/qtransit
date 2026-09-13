from pydantic import BaseModel, Field

class CompanyCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    slug: str = Field(..., min_length=2, max_length=100)
    country: str | None = None
    currency: str | None = None
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.agency import AgencyCreate, AgencyResponse
from app.services.agency_service import AgencyService

router = APIRouter(prefix="/agencies", tags=["agencies"])


@router.get("", response_model=list[AgencyResponse])
def list_agencies(company_id: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = AgencyService(db)
    return service.list_agencies(company_id=company_id, skip=skip, limit=limit)


@router.post("", response_model=AgencyResponse)
def create_agency(payload: AgencyCreate, company_id: int, db: Session = Depends(get_db)):
    service = AgencyService(db)
    agency = service.create_agency(
        company_id=company_id,
        name=payload.name,
        code=payload.code,
        city=payload.city,
        country=payload.country,
    )
    return agency


@router.get("/{agency_id}", response_model=AgencyResponse)
def get_agency(agency_id: int, db: Session = Depends(get_db)):
    service = AgencyService(db)
    return service.get_agency_by_id(agency_id)

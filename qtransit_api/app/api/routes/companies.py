from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.company_service import CompanyService
from app.schemas.company import CompanyCreateRequest

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", summary="Lister les entreprises")
def list_companies(db: Session = Depends(get_db)):
    service = CompanyService(db)
    companies = service.company_repository.get_all()
    return {"success": True, "data": companies}


@router.post("", summary="Créer une entreprise")
def create_company(payload: CompanyCreateRequest, db: Session = Depends(get_db)):
    service = CompanyService(db)
    company = service.create_company(
        name=payload.name,
        slug=payload.slug,
        country=payload.country,
        currency=payload.currency,
    )
    return {"success": True, "data": company}


@router.get("/{company_id}", summary="Détail d'une entreprise")
def get_company(company_id: int, db: Session = Depends(get_db)):
    service = CompanyService(db)
    company = service.get_company_by_id(company_id)
    return {"success": True, "data": company}

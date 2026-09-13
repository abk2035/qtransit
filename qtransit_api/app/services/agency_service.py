from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, NotFoundException
from app.core.models import Agency
from app.repositories.agency_repository import AgencyRepository
from app.services.base_service import BaseService


class AgencyService(BaseService[Agency]):
    def __init__(self, db: Session):
        super().__init__(AgencyRepository(db))
        self.agency_repository: AgencyRepository = self.repository

    def create_agency(self, company_id: int, name: str, code: str, city: str | None = None, country: str | None = None) -> Agency:
        existing = self.agency_repository.get_by_field("code", code)
        if existing and existing.company_id == company_id:
            raise ConflictException(f"Une agence avec le code '{code}' existe déjà.", error_code="agency_exists")

        agency = Agency(
            company_id=company_id,
            name=name,
            code=code,
            city=city,
            country=country,
            is_active=True,
        )
        return self.agency_repository.create(agency)

    def get_agency_by_id(self, agency_id: int) -> Agency:
        agency = self.agency_repository.get_by_id(agency_id)
        if agency is None:
            raise NotFoundException(f"Agence introuvable : {agency_id}", error_code="agency_not_found")
        return agency

    def list_agencies(self, company_id: int | None = None, skip: int = 0, limit: int | None = None):
        query = self.agency_repository.db.query(Agency)
        if company_id is not None:
            query = query.filter(Agency.company_id == company_id)
        if limit is not None:
            query = query.offset(skip).limit(limit)
        else:
            query = query.offset(skip)
        return query.all()

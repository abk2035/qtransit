from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, NotFoundException
from app.core.models import Company
from app.repositories.company_repository import CompanyRepository
from app.services.base_service import BaseService


class CompanyService(BaseService[Company]):
    def __init__(self, db: Session):
        super().__init__(CompanyRepository(db))
        self.company_repository = self.repository

    def create_company(self, name: str, slug: str, country: str | None = None, currency: str | None = None) -> Company:
        existing = self.company_repository.get_by_slug(slug)
        if existing:
            raise ConflictException(f"Une entreprise avec le slug '{slug}' existe déjà.", error_code="company_exists")

        company = Company(
            name=name,
            slug=slug,
            country=country,
            currency=currency,
            is_active=True,
        )
        return self.company_repository.create(company)

    def get_company_by_id(self, company_id: int) -> Company:
        company = self.company_repository.get_by_id(company_id)
        if company is None:
            raise NotFoundException(f"Entreprise introuvable : {company_id}", error_code="company_not_found")
        return company

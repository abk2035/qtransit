from sqlalchemy.orm import Session

from app.core.models import Company
from app.repositories.base_repository import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db: Session):
        super().__init__(db, Company)

    def get_by_slug(self, slug: str) -> Company | None:
        return self.db.query(Company).filter(Company.slug == slug).first()

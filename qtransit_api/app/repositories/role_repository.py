from sqlalchemy.orm import Session

from app.core.models import Role
from app.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self, db: Session):
        super().__init__(db, Role)

    def get_by_name_and_company(self, name: str, company_id: int) -> Role | None:
        return self.db.query(Role).filter(Role.name == name, Role.company_id == company_id).first()

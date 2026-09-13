from sqlalchemy.orm import Session

from app.core.models import Permission
from app.repositories.base_repository import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, db: Session):
        super().__init__(db, Permission)

    def get_by_code_and_company(self, code: str, company_id: int) -> Permission | None:
        return self.db.query(Permission).filter(Permission.code == code, Permission.company_id == company_id).first()

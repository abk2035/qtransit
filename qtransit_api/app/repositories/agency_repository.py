from sqlalchemy.orm import Session

from app.core.models import Agency
from app.repositories.base_repository import BaseRepository


class AgencyRepository(BaseRepository[Agency]):
    def __init__(self, db: Session):
        super().__init__(db, Agency)

    def get_by_code(self, code: str) -> Agency | None:
        return self.db.query(Agency).filter(Agency.code == code).first()

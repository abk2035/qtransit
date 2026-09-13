from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, NotFoundException
from app.core.models import Permission
from app.repositories.permission_repository import PermissionRepository
from app.services.base_service import BaseService


class PermissionService(BaseService[Permission]):
    def __init__(self, db: Session):
        super().__init__(PermissionRepository(db))
        self.permission_repository: PermissionRepository = self.repository

    def create_permission(self, company_id: int, code: str, name: str, module_name: str, action_name: str) -> Permission:
        existing = self.permission_repository.get_by_code_and_company(code, company_id)
        if existing:
            raise ConflictException(f"Une permission avec le code '{code}' existe déjà.", error_code="permission_exists")

        perm = Permission(
            company_id=company_id,
            code=code,
            name=name,
            module_name=module_name,
            action_name=action_name,
            is_active=True,
        )
        return self.permission_repository.create(perm)

    def get_permission_by_id(self, permission_id: int) -> Permission:
        perm = self.permission_repository.get_by_id(permission_id)
        if perm is None:
            raise NotFoundException(f"Permission introuvable : {permission_id}", error_code="permission_not_found")
        return perm

    def list_permissions(self, company_id: int | None = None, skip: int = 0, limit: int | None = None):
        query = self.permission_repository.db.query(Permission)
        if company_id is not None:
            query = query.filter(Permission.company_id == company_id)
        if limit is not None:
            query = query.offset(skip).limit(limit)
        else:
            query = query.offset(skip)
        return query.all()

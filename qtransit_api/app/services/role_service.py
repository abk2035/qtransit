from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, NotFoundException
from app.core.models import Role
from app.repositories.role_repository import RoleRepository
from app.services.base_service import BaseService
from app.repositories.permission_repository import PermissionRepository


class RoleService(BaseService[Role]):
    def __init__(self, db: Session):
        super().__init__(RoleRepository(db))
        self.role_repository: RoleRepository = self.repository

    def create_role(self, company_id: int, name: str, description: str | None = None) -> Role:
        existing = self.role_repository.get_by_name_and_company(name, company_id)
        if existing:
            raise ConflictException(f"Un rôle '{name}' existe déjà pour cette entreprise.", error_code="role_exists")

        role = Role(company_id=company_id, name=name, description=description, is_active=True)
        return self.role_repository.create(role)

    def get_role_by_id(self, role_id: int) -> Role:
        role = self.role_repository.get_by_id(role_id)
        if role is None:
            raise NotFoundException(f"Rôle introuvable : {role_id}", error_code="role_not_found")
        return role

    def list_roles(self, company_id: int | None = None, skip: int = 0, limit: int | None = None):
        query = self.role_repository.db.query(Role)
        if company_id is not None:
            query = query.filter(Role.company_id == company_id)
        if limit is not None:
            query = query.offset(skip).limit(limit)
        else:
            query = query.offset(skip)
        return query.all()

    def add_permission_to_role(self, role_id: int, permission) -> Role:
        """Attach a Permission object or id to a Role."""
        role = self.get_role_by_id(role_id)
        db = self.role_repository.db

        perm_obj = permission
        if not hasattr(permission, "id"):
            perm_obj = PermissionRepository(db).get_by_id(int(permission))

        if perm_obj is None:
            raise NotFoundException(f"Permission introuvable : {permission}", error_code="permission_not_found")

        if perm_obj in role.permissions:
            raise ConflictException("Permission déjà attachée au rôle", error_code="permission_already_attached")

        role.permissions.append(perm_obj)
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    def remove_permission_from_role(self, role_id: int, permission_id: int) -> None:
        role = self.get_role_by_id(role_id)
        db = self.role_repository.db
        perm = db.query(type(role.permissions[0]) if role.permissions else None).filter_by(id=permission_id).first() if role.permissions else None
        perm = PermissionRepository(db).get_by_id(permission_id)
        if perm is None or perm not in role.permissions:
            raise NotFoundException("Permission non attachée au rôle", error_code="permission_not_attached")

        role.permissions.remove(perm)
        db.add(role)
        db.commit()
        return None

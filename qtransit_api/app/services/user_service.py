from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, NotFoundException
from app.core.models import User
from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.repositories.role_repository import RoleRepository


class UserService(BaseService[User]):
    def __init__(self, db: Session):
        super().__init__(UserRepository(db))
        self.user_repository: UserRepository = self.repository

    def create_user(self, email: str, password: str, first_name: str, last_name: str, company_id: int | None = None, agency_id: int | None = None) -> User:
        existing = self.user_repository.get_by_email(email)
        if existing:
            raise ConflictException(f"Un utilisateur avec l'email '{email}' existe déjà.", error_code="user_exists")

        user = User(
            email=email,
            password_hash=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            company_id=company_id,
            agency_id=agency_id,
            user_type="user",
            is_active=True,
        )
        return self.user_repository.create(user)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundException(f"Utilisateur introuvable : {user_id}", error_code="user_not_found")
        return user

    def list_users(self, skip: int = 0, limit: int | None = None):
        return self.user_repository.db.query(User).offset(skip).limit(limit if limit else 100).all()

    def update_user(self, user_id: int, data: dict) -> User:
        user = self.get_user_by_id(user_id)
        for k, v in data.items():
            if v is not None and hasattr(user, k):
                setattr(user, k, v)
        return self.user_repository.update(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        self.user_repository.delete(user)

    def assign_role_to_user(self, user_id: int, role_id: int):
        """Assign a role to a user by ids."""
        user = self.get_user_by_id(user_id)
        db = self.user_repository.db
        role = RoleRepository(db).get_by_id(role_id)
        if role is None:
            raise NotFoundException(f"Rôle introuvable : {role_id}", error_code="role_not_found")

        if role in user.roles:
            raise ConflictException("Rôle déjà assigné à l'utilisateur", error_code="role_already_assigned")

        user.roles.append(role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def remove_role_from_user(self, user_id: int, role_id: int):

        user = self.get_user_by_id(user_id)
        db = self.user_repository.db
        role = RoleRepository(db).get_by_id(role_id)
        if role is None or role not in user.roles:
            raise NotFoundException("Rôle non assigné à l'utilisateur", error_code="role_not_assigned")

        user.roles.remove(role)
        db.add(user)
        db.commit()
        return None

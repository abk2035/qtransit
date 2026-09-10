from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedException
from app.core.models import User
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def login(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedException("Identifiants invalides", error_code="invalid_credentials")

        if not user.is_active:
            raise UnauthorizedException("Compte inactif", error_code="inactive_account")

        token = create_access_token(
            {"sub": user.email, "user_type": user.user_type},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return token

    def get_current_user_from_token(self, token: str) -> User:
        from app.core.security import decode_access_token

        try:
            payload = decode_access_token(token)
            email = payload.get("sub")
            if not email:
                raise ValueError("Token invalide")
        except Exception as exc:
            raise UnauthorizedException("Jeton invalide", error_code="invalid_token") from exc

        user = self.user_repository.get_by_email(email)
        if user is None or not user.is_active:
            raise UnauthorizedException("Utilisateur introuvable ou inactif", error_code="user_not_found")

        return user

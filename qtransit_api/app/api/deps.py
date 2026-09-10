from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.models import User
from app.core.security import oauth2_scheme
from app.db.session import get_db
from app.services.auth_service import AuthService


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    auth_service = AuthService(db)
    return auth_service.get_current_user_from_token(token)

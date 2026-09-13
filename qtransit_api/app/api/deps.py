from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.models import User
from app.core.security import oauth2_scheme
from app.db.session import get_db
from app.services.auth_service import AuthService
from fastapi import HTTPException, status


def require_permission(permission_code: str):
    """Return a dependency callable that ensures the current user has the given permission code.

    Usage in routes:
        @router.get("/...")
        def handler(..., _=Depends(require_permission("some_permission"))):
            ...
    """

    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> bool:
        # super admins bypass checks
        if getattr(current_user, "is_super_admin", False):
            return True

        # check roles and permissions loaded on the user
        for role in getattr(current_user, "roles", []):
            for perm in getattr(role, "permissions", []):
                if perm.code == permission_code and getattr(perm, "is_active", True):
                    return True

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return dependency


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    auth_service = AuthService(db)
    return auth_service.get_current_user_from_token(token)

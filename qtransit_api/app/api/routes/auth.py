from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.models import User
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse, UserMeResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    token = auth_service.login(payload.email, payload.password)
    return TokenResponse(access_token=token, token_type="bearer", expires_in=3600)


@router.get("/me", response_model=UserMeResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user

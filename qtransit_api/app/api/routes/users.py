from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = UserService(db)
    users = service.list_users(skip=skip, limit=limit)
    return users


@router.post("", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.create_user(
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
        company_id=payload.company_id,
        agency_id=payload.agency_id,
    )
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.update_user(user_id, payload.dict())
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    service.delete_user(user_id)
    return {"success": True}


@router.post("/{user_id}/roles", summary="Assign a role to a user")
def assign_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.assign_role_to_user(user_id, role_id)
    return user


@router.delete("/{user_id}/roles/{role_id}", summary="Remove a role from a user")
def remove_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    service.remove_role_from_user(user_id, role_id)
    return {"success": True}

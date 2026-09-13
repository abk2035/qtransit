from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.permission import PermissionCreate, PermissionResponse
from app.services.permission_service import PermissionService

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("", response_model=list[PermissionResponse])
def list_permissions(company_id: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = PermissionService(db)
    return service.list_permissions(company_id=company_id, skip=skip, limit=limit)


@router.post("", response_model=PermissionResponse)
def create_permission(payload: PermissionCreate, db: Session = Depends(get_db)):
    service = PermissionService(db)
    perm = service.create_permission(
        company_id=payload.company_id,
        code=payload.code,
        name=payload.name,
        module_name=payload.module_name,
        action_name=payload.action_name,
    )
    return perm


@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    service = PermissionService(db)
    return service.get_permission_by_id(permission_id)

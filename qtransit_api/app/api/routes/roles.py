from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.role import RoleCreate, RoleResponse
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleResponse])
def list_roles(company_id: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = RoleService(db)
    return service.list_roles(company_id=company_id, skip=skip, limit=limit)


@router.post("", response_model=RoleResponse)
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    service = RoleService(db)
    role = service.create_role(company_id=payload.company_id, name=payload.name, description=payload.description)
    return role


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    service = RoleService(db)
    return service.get_role_by_id(role_id)


@router.post("/{role_id}/permissions", summary="Attach a permission to a role")
def attach_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    service = RoleService(db)
    role = service.add_permission_to_role(role_id, permission_id)
    return role


@router.delete("/{role_id}/permissions/{permission_id}", summary="Detach a permission from a role")
def detach_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    service = RoleService(db)
    service.remove_permission_from_role(role_id, permission_id)
    return {"success": True}

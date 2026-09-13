from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.core.models import Company, Permission, Role, User
from app.core.security import get_password_hash
from app.services.role_service import RoleService
from app.services.user_service import UserService


def setup_in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_assign_permission_and_role():
    db = setup_in_memory_db()

    # create company
    company = Company(name="TestCo", slug="testco")
    db.add(company)
    db.commit()
    db.refresh(company)

    # create permission
    perm = Permission(company_id=company.id, code="can_view", name="Can View", module_name="core", action_name="view", is_active=True)
    db.add(perm)
    db.commit()
    db.refresh(perm)

    # create role
    role = Role(company_id=company.id, name="admin", description="Admin role")
    db.add(role)
    db.commit()
    db.refresh(role)

    # create user
    user = User(email="user@example.com", password_hash=get_password_hash("pwd"), first_name="First", last_name="Last", company_id=company.id)
    db.add(user)
    db.commit()
    db.refresh(user)

    # attach permission to role
    rs = RoleService(db)
    rs.add_permission_to_role(role.id, perm.id)
    role_db = rs.get_role_by_id(role.id)
    assert any(p.code == "can_view" for p in role_db.permissions)

    # assign role to user
    us = UserService(db)
    us.assign_role_to_user(user.id, role.id)
    user_db = us.get_user_by_id(user.id)
    assert any(r.name == "admin" for r in user_db.roles)

    # ensure permission is visible through user roles
    perms = [p.code for r in user_db.roles for p in r.permissions]
    assert "can_view" in perms

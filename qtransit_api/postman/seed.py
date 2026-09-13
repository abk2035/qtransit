"""
Run this seeder to populate PostgreSQL with minimal RBAC data for manual Postman testing.
Usage:
    python postman/seed.py

It reads the `DATABASE_URL` from environment or uses the `DATABASE_URL` in the Postman environment file.
"""
import os

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.core.models import Company, Permission, Role, User
from app.core.security import get_password_hash


def run():
    print("Creating tables (if not exist) and seeding data...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # company
    company = db.query(Company).filter(Company.slug == "testco").first()
    if not company:
        company = Company(name="TestCo", slug="testco", country="FR", currency="EUR", is_active=True)
        db.add(company)
        db.commit()
        db.refresh(company)
        print("Created company", company.id)
    else:
        print("Company exists", company.id)

    # permissions
    perm = db.query(Permission).filter(Permission.code == "can_view", Permission.company_id == company.id).first()
    if not perm:
        perm = Permission(company_id=company.id, code="can_view", name="Can View", module_name="core", action_name="view", is_active=True)
        db.add(perm)
        db.commit()
        db.refresh(perm)
        print("Created permission", perm.id)
    else:
        print("Permission exists", perm.id)

    # role
    role = db.query(Role).filter(Role.name == "admin", Role.company_id == company.id).first()
    if not role:
        role = Role(company_id=company.id, name="admin", description="Administrator role", is_active=True)
        db.add(role)
        db.commit()
        db.refresh(role)
        print("Created role", role.id)
    else:
        print("Role exists", role.id)

    # attach permission to role
    if perm not in role.permissions:
        role.permissions.append(perm)
        db.add(role)
        db.commit()
        print("Attached permission to role")
    else:
        print("Permission already attached to role")

    # user
    user = db.query(User).filter(User.email == "rbac_user@example.com").first()
    if not user:
        user = User(email="rbac_user@example.com", password_hash=get_password_hash("password"), first_name="RBAC", last_name="User", company_id=company.id, is_active=True)
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Created user", user.id)
    else:
        print("User exists", user.id)

    # assign role to user
    if role not in user.roles:
        user.roles.append(role)
        db.add(user)
        db.commit()
        print("Assigned role to user")
    else:
        print("Role already assigned to user")

    db.close()


if __name__ == "__main__":
    run()

from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.core.models import Agency, Company, Permission, Role, User


def test_core_models_are_created_and_linked():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    company = Company(
        name="QTransit Dakar",
        slug="qtransit-dakar",
        country="Senegal",
        currency="XOF",
        timezone="Africa/Dakar",
    )

    agency = Agency(
        name="Agence Centre",
        code="DCK-01",
        company=company,
        city="Dakar",
        country="Senegal",
    )

    role = Role(name="admin", company=company)
    permission = Permission(
        code="users.create",
        name="Créer un utilisateur",
        module_name="core",
        action_name="create",
        company=company,
    )
    role.permissions.append(permission)

    user = User(
        email="admin@qtransit.sn",
        first_name="Moussa",
        last_name="Diop",
        password_hash="hashed_password",
        is_active=True,
        company=company,
        agency=agency,
        created_at=datetime.now(timezone.utc),
    )
    user.roles.append(role)

    with Session(engine) as session:
        session.add_all([company, agency, role, permission, user])
        session.commit()
        session.refresh(user)

        stored_user = session.get(User, user.id)
        assert stored_user is not None
        assert stored_user.company.name == "QTransit Dakar"
        assert stored_user.agency.name == "Agence Centre"
        assert len(stored_user.roles) == 1
        assert stored_user.roles[0].name == "admin"
        assert stored_user.roles[0].permissions[0].code == "users.create"

        stored_company = session.get(Company, company.id)
        assert stored_company is not None
        assert stored_company.agencies[0].code == "DCK-01"

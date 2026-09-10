"""add user types

Revision ID: 5f67a6c1f80d
Revises: ee60c1754261
Create Date: 2026-09-05 20:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5f67a6c1f80d"
down_revision = "ee60c1754261"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("user_type", sa.String(length=30), nullable=False, server_default="user"))
    op.alter_column("users", "company_id", existing_type=sa.Integer(), nullable=True)
    op.create_index(op.f("ix_users_user_type"), "users", ["user_type"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_user_type"), table_name="users")
    op.alter_column("users", "company_id", existing_type=sa.Integer(), nullable=False)
    op.drop_column("users", "user_type")

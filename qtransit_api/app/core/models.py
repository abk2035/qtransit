from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SubscriptionStatus(str):
    ACTIVE = "active"
    TRIAL = "trial"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class BillingCycle(str):
    MONTHLY = "monthly"
    ANNUAL = "annual"


class UserType(str):
    """Type d’utilisateur au sein de la plateforme SaaS."""


UserRoleType = str


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(80), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="company")
    roles: Mapped[List["Role"]] = relationship(back_populates="company")
    permissions: Mapped[List["Permission"]] = relationship(back_populates="company")
    agencies: Mapped[List["Agency"]] = relationship(back_populates="company")
    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="company")


class Agency(Base):
    __tablename__ = "agencies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    company: Mapped[Company] = relationship(back_populates="agencies")
    users: Mapped[List["User"]] = relationship(back_populates="agency")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    company: Mapped[Company] = relationship(back_populates="roles")
    users: Mapped[List["User"]] = relationship(back_populates="roles", secondary=user_roles)
    permissions: Mapped[List["Permission"]] = relationship(back_populates="roles", secondary="role_permissions")


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    module_name: Mapped[str] = mapped_column(String(80), nullable=False)
    action_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    company: Mapped[Company] = relationship(back_populates="permissions")
    roles: Mapped[List[Role]] = relationship(back_populates="permissions", secondary="role_permissions")


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True)
    agency_id: Mapped[int | None] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    user_type: Mapped[str] = mapped_column(String(30), nullable=False, default="user", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    company: Mapped[Company | None] = relationship(back_populates="users")
    agency: Mapped[Agency | None] = relationship(back_populates="users")
    roles: Mapped[List[Role]] = relationship(back_populates="users", secondary=user_roles)

    @property
    def is_super_admin(self) -> bool:
        return self.user_type == "super_admin" or self.is_superuser

    @property
    def is_company_admin(self) -> bool:
        return self.user_type == "company_admin" and self.company_id is not None

    @property
    def is_agency_admin(self) -> bool:
        return self.user_type == "agency_admin" and self.company_id is not None and self.agency_id is not None

    @property
    def is_standard_user(self) -> bool:
        return self.user_type == "user"


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    monthly_price: Mapped[float] = mapped_column(default=0.0, nullable=False)
    annual_price: Mapped[float] = mapped_column(default=0.0, nullable=False)
    billing_cycle: Mapped[str] = mapped_column(String(20), default=BillingCycle.MONTHLY, nullable=False)
    max_users: Mapped[int | None] = mapped_column(nullable=True)
    max_agencies: Mapped[int | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="plan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    plan_id: Mapped[int] = mapped_column(ForeignKey("subscription_plans.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default=SubscriptionStatus.TRIAL, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    trial_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    company: Mapped[Company] = relationship(back_populates="subscriptions")
    plan: Mapped[SubscriptionPlan] = relationship(back_populates="subscriptions")
    features: Mapped[List["SubscriptionFeature"]] = relationship(back_populates="subscription")


class Feature(Base):
    __tablename__ = "features"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    module_name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    subscription_features: Mapped[List["SubscriptionFeature"]] = relationship(back_populates="feature")


class SubscriptionFeature(Base):
    __tablename__ = "subscription_features"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"), nullable=False)
    feature_id: Mapped[int] = mapped_column(ForeignKey("features.id"), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    quota: Mapped[int | None] = mapped_column(nullable=True)
    used_count: Mapped[int] = mapped_column(default=0, nullable=False)

    subscription: Mapped[Subscription] = relationship(back_populates="features")
    feature: Mapped[Feature] = relationship(back_populates="subscription_features")

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.db.base import Base

# Generic type variable bound to SQLAlchemy declarative `Base`.
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD helpers for SQLAlchemy models.

    This base class is intended to be subclassed by concrete repositories that
    pass a specific SQLAlchemy model class to the constructor. It centralizes
    common data-access patterns so services can remain thin and focused on
    business logic.
    """

    def __init__(self, db: Session, model: type[ModelType]):
        """Initialize repository with a DB session and the model class.

        Args:
            db: SQLAlchemy Session instance used for queries and transactions.
            model: The SQLAlchemy model (declarative) class this repository manages.
        """
        self.db = db
        self.model = model

    def get_by_id(self, obj_id: int) -> ModelType | None:
        """Return a single model instance by its primary key id, or None.

        Performs a simple query filtering on `model.id`.
        """
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self, skip: int = 0, limit: int | None = None):
        """Return a list of model instances with optional pagination.

        Args:
            skip: Number of records to skip (offset).
            limit: Maximum number of records to return. If None, no limit is applied.
        """
        query = self.db.query(self.model).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def create(self, obj: ModelType) -> ModelType:
        """Persist a new model instance and return it refreshed from the DB.

        The instance should be a model object (not a dict). This method commits
        the transaction and refreshes the instance so generated fields (like id
        or timestamps) are populated.
        """
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        """Persist changes made to a model instance and return the refreshed object.

        Note: the caller is expected to have modified fields on the `obj`.
        """
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        """Remove the given model instance from the database and commit."""
        self.db.delete(obj)
        self.db.commit()

    def get_by_field(self, field_name: str, value: object) -> ModelType | None:
        """Generic helper to query a single instance by an arbitrary field name.

        Example: `repo.get_by_field('email', 'foo@example.com')`.
        """
        field = getattr(self.model, field_name)
        return self.db.query(self.model).filter(field == value).first()

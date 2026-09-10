from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def get_by_id(self, obj_id: int) -> ModelType | None:
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self, skip: int = 0, limit: int | None = None):
        query = self.db.query(self.model).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.commit()

    def get_by_field(self, field_name: str, value: object) -> ModelType | None:
        field = getattr(self.model, field_name)
        return self.db.query(self.model).filter(field == value).first()

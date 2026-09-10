from typing import Generic, TypeVar

from app.core.exceptions import AppException

T = TypeVar("T")


class BaseService(Generic[T]):
    def __init__(self, repository):
        self.repository = repository

    def _ensure_found(self, obj: T | None, message: str = "Ressource introuvable", error_code: str = "not_found") -> T:
        if obj is None:
            raise AppException(message=message, status_code=404, error_code=error_code)
        return obj

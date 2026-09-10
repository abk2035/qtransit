from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.routes.auth import router as auth_router
from app.api.routes.companies import router as companies_router
from app.core.error_handlers import (
    app_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)
from app.core.exceptions import AppException

app = FastAPI(title="QTransit API", version="0.1.0")

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth_router)
app.include_router(companies_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

from fastapi import status


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "internal_error",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class BadRequestException(AppException):
    def __init__(self, message: str, error_code: str = "bad_request"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, error_code=error_code)


class UnauthorizedException(AppException):
    def __init__(self, message: str, error_code: str = "unauthorized"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED, error_code=error_code)


class ForbiddenException(AppException):
    def __init__(self, message: str, error_code: str = "forbidden"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN, error_code=error_code)


class NotFoundException(AppException):
    def __init__(self, message: str, error_code: str = "not_found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND, error_code=error_code)


class ConflictException(AppException):
    def __init__(self, message: str, error_code: str = "conflict"):
        super().__init__(message=message, status_code=status.HTTP_409_CONFLICT, error_code=error_code)


class ValidationException(AppException):
    def __init__(self, message: str, error_code: str = "validation_error"):
        super().__init__(message=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, error_code=error_code)


class InternalServerErrorException(AppException):
    def __init__(self, message: str = "Une erreur interne est survenue", error_code: str = "internal_server_error"):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_code=error_code)

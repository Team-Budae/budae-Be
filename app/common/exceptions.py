from fastapi import HTTPException


class LocalHubException(Exception):
    """서비스 전반에서 사용하는 기본 예외."""

    def __init__(self, message: str, status_code: int = 500, code: str = "internal_error", details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}


class NotFoundError(LocalHubException):
    def __init__(self, message: str = "리소스를 찾을 수 없습니다.", code: str = "not_found"):
        super().__init__(message=message, status_code=404, code=code)


class ValidationError(LocalHubException):
    def __init__(self, message: str = "입력값이 올바르지 않습니다.", code: str = "validation_error"):
        super().__init__(message=message, status_code=400, code=code)


class ConflictError(LocalHubException):
    def __init__(self, message: str = "이미 존재하는 리소스입니다.", code: str = "conflict"):
        super().__init__(message=message, status_code=409, code=code)


class ForbiddenError(LocalHubException):
    def __init__(self, message: str = "권한이 없습니다.", code: str = "forbidden"):
        super().__init__(message=message, status_code=403, code=code)


class UnauthorizedError(LocalHubException):
    def __init__(self, message: str = "인증이 필요합니다.", code: str = "unauthorized"):
        super().__init__(message=message, status_code=401, code=code)


def raise_http_exception(exc: LocalHubException) -> None:
    raise HTTPException(status_code=exc.status_code, detail={"code": exc.code, "message": exc.message, "details": exc.details})

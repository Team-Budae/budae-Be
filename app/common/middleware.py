from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.common.exceptions import LocalHubException
from app.core.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(LocalHubException)
    async def localhub_exception_handler(request: Request, exc: LocalHubException):
        logger.warning("Handled exception: %s", exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": {"code": exc.code, "message": exc.message, "details": exc.details}},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": {"code": "internal_error", "message": "서버 내부 오류가 발생했습니다."}},
        )

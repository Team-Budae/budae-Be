from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.common.middleware import register_exception_handlers
from app.core.config import settings
from app.core.logging import get_logger
from app.domains.category.router import router as category_router
from app.domains.chat.router import router as chat_router
from app.domains.comment.router import router as comment_router
from app.domains.data_source.router import router as data_source_router
from app.domains.dashboard.router import router as dashboard_router
from app.domains.place.router import router as place_router
from app.domains.post.router import router as post_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("%s started", settings.APP_NAME)
    from app.scripts.init_db import init_db

    init_db()
    yield
    logger.info("Server shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(place_router, prefix="/api")
app.include_router(post_router, prefix="/api")
app.include_router(comment_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(data_source_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "ok",
    }
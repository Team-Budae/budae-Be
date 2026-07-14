from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 시작 시 실행되는 영역
    - DB 초기화
    - JSON Import
    - 모델 생성
    """
    print("🚀 LocalHub API Started")

    yield

    print("🛑 LocalHub API Shutdown")


app = FastAPI(
    title="LocalHub API",
    description="AI 기반 지역 관광 커뮤니티 API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vue 개발 서버
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to LocalHub API",
        "status": "running",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
    }
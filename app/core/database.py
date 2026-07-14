# SQLite와 통신하는 모든 기능의 중심
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# SQLite Engine 생성
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 전용 옵션
    echo=True,  # 개발 중 SQL 로그 출력, 배포시 False로 변경
)


# DB Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# 모든 Model이 상속받을 Base
class Base(DeclarativeBase):
    pass


# Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
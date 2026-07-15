import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# 현재 config.py 위치를 기준으로 프로젝트 최상위(루트) 디렉터리 경로 계산
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABS_DB_PATH = os.path.join(BASE_DIR, "app", "db.sqlite3")

class Settings(BaseSettings):
    APP_NAME: str = "LocalHub API"
    APP_VERSION: str = "1.0.0"
    
    # 동적 절대 경로 적용
    DATABASE_URL: str = f"sqlite:///{ABS_DB_PATH}"
    
    OPENAI_API_KEY: str = ""
    FRONTEND_URL: str = "http://localhost:5173"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
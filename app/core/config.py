import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# 현재 config.py 위치를 기준으로 프로젝트 최상위(루트) 디렉터리 경로를 구합니다.
# (구조에 따라 os.path.dirname의 중첩 횟수를 조절해 루트 폴더를 가리키도록 설정합니다.)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABS_DB_PATH = os.path.join(BASE_DIR, "app", "db.sqlite3")

class Settings(BaseSettings):
    APP_NAME: str = "LocalHub API"[cite: 1]
    APP_VERSION: str = "1.0.0"[cite: 1]
    
    # 기본 상대 경로 대신 동적으로 빌드된 절대 경로를 기본값으로 지정합니다.
    DATABASE_URL: str = f"sqlite:///{ABS_DB_PATH}"
    
    OPENAI_API_KEY: str = ""[cite: 1]
    FRONTEND_URL: str = "http://localhost:5173"[cite: 1]
    LOG_LEVEL: str = "INFO"[cite: 1]
    DEBUG: bool = False[cite: 1]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

settings = Settings()[cite: 1]
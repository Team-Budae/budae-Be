import json
from pathlib import Path

from app.core.database import Base, engine, SessionLocal
from app.domains.category.models import Category
from app.domains.chat.models import ChatMessage, ChatSession
from app.domains.comment.models import Comment
from app.domains.data_source.models import DataSource
from app.domains.place.models import Place
from app.domains.post.models import Post
from app.scripts.import_seoul_data import import_seoul_data

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "서울"

def init_db() -> None:
    # 1. 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 2. 세션을 열고 초기 더미/수집 데이터 입력 진행
    db = SessionLocal()
    try:
        if db.query(Place).first() is None:
            print("📦 기존 데이터가 없습니다. 서울 데이터 JSON 파일을 DB에 등록합니다...")
            result = import_seoul_data()
            imported = result.get("imported", 0)
            if imported:
                print(f"✅ {imported}개의 Place 데이터를 성공적으로 입력했습니다!")
            else:
                print("⚠️ 서울 데이터 JSON 파일이 없거나 새로운 Place 데이터가 없습니다.")
        else:
            print("ℹ️ 이미 데이터베이스에 데이터가 존재합니다. 초기화를 건너뜁니다.")
    except Exception as e:
        db.rollback()
        print(f"❌ 데이터 초기화 중 오류 발생: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized")
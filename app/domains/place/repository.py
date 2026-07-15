from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.domains.place.models import Place


class PlaceRepository(BaseRepository[Place]):
    def __init__(self, session: Session):
        super().__init__(session, Place)

    def get_by_content_id(self, content_id: str, content_type_id: int | None = None) -> Place | None:
        query = self.session.query(Place).filter(Place.content_id == content_id)
        if content_type_id is not None:
            query = query.filter(Place.content_type_id == content_type_id)
        return query.first()

    def search(self, keyword: str | None = None, content_type_id: int | None = None, *, skip: int = 0, limit: int = 20) -> tuple[list[Place], int]:
        query = self.session.query(Place)
        
        # 키워드 필터링
        if keyword:
            like_pattern = f"%{keyword}%"
            query = query.filter(
                (Place.title.like(like_pattern)) |
                (Place.addr1.like(like_pattern)) |
                (Place.district_name.like(like_pattern))
            )
            
        # 카테고리(content_type_id) 필터링 추가
        if content_type_id is not None:
            query = query.filter(Place.content_type_id == content_type_id)
            
        # 전체 개수 조회
        total = query.count()
        # 데이터 조회
        items = query.offset(skip).limit(limit).all()
        
        return items, total
        

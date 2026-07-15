from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domains.dashboard.schemas import DashboardResponse
from app.domains.place.models import Place
from app.domains.place.repository import PlaceRepository
from app.domains.post.repository import PostRepository

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_dashboard_data(db: Session = Depends(get_db)) -> dict:
    place_repo = PlaceRepository(db)
    post_repo = PostRepository(db)

    top_places = place_repo.search(keyword=None, content_type_id=None, skip=0, limit=3)[0]
    festival_places = place_repo.search(keyword=None, content_type_id=15, skip=0, limit=3)[0]
    pins = place_repo.search(keyword=None, content_type_id=None, skip=0, limit=24)[0]

    place_count = db.query(Place).count()
    festival_count = place_repo.search(keyword=None, content_type_id=15, skip=0, limit=1)[1]
    community_posts_count = post_repo.list_posts(skip=0, limit=1)[1]
    type_counts = {
        "attraction": place_repo.search(keyword=None, content_type_id=12, skip=0, limit=1)[1],
        "nature": place_repo.search(keyword=None, content_type_id=28, skip=0, limit=1)[1],
        "accommodation": place_repo.search(keyword=None, content_type_id=32, skip=0, limit=1)[1],
    }

    return {
        "places": top_places,
        "festivals": festival_places,
        "pins": pins,
        "stats": {
            "place_count": place_count,
            "festival_count": festival_count,
            "community_posts_count": community_posts_count,
            "type_counts": type_counts,
        },
    }


@router.get("", response_model=DashboardResponse, summary="대시보드 데이터 조회")
async def get_dashboard(service: dict = Depends(get_dashboard_data)):
    return service

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.schemas import BaseResponse, PaginatedResponse
from app.core.database import get_db
from app.domains.place.repository import PlaceRepository
from app.domains.place.schemas import PlaceCreate, PlaceRead, PlaceUpdate
from app.domains.place.service import PlaceService

router = APIRouter(prefix="/places", tags=["places"])


def get_place_service(db: Session = Depends(get_db)) -> PlaceService:
    repository = PlaceRepository(db)
    return PlaceService(repository)


@router.get("", response_model=PaginatedResponse[PlaceRead], summary="장소 목록 조회")
async def list_places(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=10000),
    keyword: str | None = Query(default=None, description="이름 또는 주소 검색어"),
    content_type_id: int | None = Query(default=None, description="카테고리 ID 필터링"),
    service: PlaceService = Depends(get_place_service),
):
    items, total = service.get_places_list(keyword=keyword, content_type_id=content_type_id, skip=skip, limit=limit)
    
    return {
        "items": [PlaceRead.model_validate(item) for item in items],
        "pagination": {
            "page": (skip // limit) + 1 if limit else 1, 
            "size": limit, 
            "total": total,
        },
    }


@router.get("/{place_id}", response_model=PlaceRead, summary="장소 상세 조회")
async def get_place(place_id: int, service: PlaceService = Depends(get_place_service)):
    place = service.get_place(place_id)
    return PlaceRead.model_validate(place)


@router.post("", response_model=PlaceRead, status_code=status.HTTP_201_CREATED, summary="장소 생성")
async def create_place(payload: PlaceCreate, service: PlaceService = Depends(get_place_service)):
    place = service.create_place(payload)
    return PlaceRead.model_validate(place)


@router.patch("/{place_id}", response_model=PlaceRead, summary="장소 수정")
async def update_place(place_id: int, payload: PlaceUpdate, service: PlaceService = Depends(get_place_service)):
    place = service.update_place(place_id, payload)
    return PlaceRead.model_validate(place)


@router.delete("/{place_id}", response_model=BaseResponse, summary="장소 삭제")
async def delete_place(place_id: int, service: PlaceService = Depends(get_place_service)):
    service.delete_place(place_id)
    return BaseResponse(message="장소가 삭제되었습니다.")

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.schemas import BaseResponse, PaginatedResponse
from app.core.database import get_db
from app.domains.category.repository import CategoryRepository
from app.domains.category.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.domains.category.service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    repository = CategoryRepository(db)
    return CategoryService(repository)


@router.get("", response_model=PaginatedResponse[CategoryRead], summary="카테고리 목록 조회")
async def list_categories(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=10000),
    service: CategoryService = Depends(get_category_service),
):
    items = service.list_categories(skip=skip, limit=limit)
    return {
        "items": [CategoryRead.model_validate(item) for item in items],
        "pagination": {"page": (skip // limit) + 1 if limit else 1, "size": limit, "total": len(items)},
    }


@router.get("/{category_id}", response_model=CategoryRead, summary="카테고리 상세 조회")
async def get_category(category_id: int, service: CategoryService = Depends(get_category_service)):
    return CategoryRead.model_validate(service.get_category(category_id))


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED, summary="카테고리 생성")
async def create_category(payload: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    category = service.create_category(payload)
    return CategoryRead.model_validate(category)


@router.patch("/{category_id}", response_model=CategoryRead, summary="카테고리 수정")
async def update_category(category_id: int, payload: CategoryUpdate, service: CategoryService = Depends(get_category_service)):
    category = service.update_category(category_id, payload)
    return CategoryRead.model_validate(category)


@router.delete("/{category_id}", response_model=BaseResponse, summary="카테고리 삭제")
async def delete_category(category_id: int, service: CategoryService = Depends(get_category_service)):
    service.delete_category(category_id)
    return BaseResponse(message="카테고리가 삭제되었습니다.")

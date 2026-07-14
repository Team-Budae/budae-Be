from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.schemas import BaseResponse, PaginatedResponse
from app.core.database import get_db
from app.domains.post.repository import PostRepository
from app.domains.post.schemas import PostCreate, PostRead, PostUpdate
from app.domains.post.service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    repository = PostRepository(db)
    return PostService(repository)


@router.get("", response_model=PaginatedResponse[PostRead], summary="게시글 목록 조회")
async def list_posts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    service: PostService = Depends(get_post_service),
):
    items = service.list_posts(skip=skip, limit=limit)
    return {
        "items": [PostRead.model_validate(item) for item in items],
        "pagination": {"page": (skip // limit) + 1 if limit else 1, "size": limit, "total": len(items)},
    }


@router.get("/{post_id}", response_model=PostRead, summary="게시글 상세 조회")
async def get_post(post_id: int, service: PostService = Depends(get_post_service)):
    return PostRead.model_validate(service.get_post(post_id))


@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED, summary="게시글 작성")
async def create_post(payload: PostCreate, service: PostService = Depends(get_post_service)):
    post = service.create_post(payload)
    return PostRead.model_validate(post)


@router.patch("/{post_id}", response_model=PostRead, summary="게시글 수정")
async def update_post(post_id: int, payload: PostUpdate, service: PostService = Depends(get_post_service)):
    post = service.update_post(post_id, payload)
    return PostRead.model_validate(post)


@router.delete("/{post_id}", response_model=BaseResponse, summary="게시글 삭제")
async def delete_post(post_id: int, password: str, service: PostService = Depends(get_post_service)):
    service.delete_post(post_id, password)
    return BaseResponse(message="게시글이 삭제되었습니다.")

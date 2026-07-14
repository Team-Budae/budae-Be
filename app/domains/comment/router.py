from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.schemas import BaseResponse
from app.core.database import get_db
from app.domains.comment.repository import CommentRepository
from app.domains.comment.schemas import CommentCreate, CommentRead, CommentUpdate
from app.domains.comment.service import CommentService

router = APIRouter(prefix="/comments", tags=["comments"])


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    repository = CommentRepository(db)
    return CommentService(repository)


@router.get("/posts/{post_id}", response_model=list[CommentRead], summary="댓글 목록 조회")
async def list_comments(post_id: int, service: CommentService = Depends(get_comment_service)):
    return [CommentRead.model_validate(item) for item in service.list_comments(post_id)]


@router.post("", response_model=CommentRead, status_code=status.HTTP_201_CREATED, summary="댓글 작성")
async def create_comment(payload: CommentCreate, service: CommentService = Depends(get_comment_service)):
    comment = service.create_comment(payload)
    return CommentRead.model_validate(comment)


@router.patch("/{comment_id}", response_model=CommentRead, summary="댓글 수정")
async def update_comment(comment_id: int, payload: CommentUpdate, service: CommentService = Depends(get_comment_service)):
    comment = service.update_comment(comment_id, payload)
    return CommentRead.model_validate(comment)


@router.delete("/{comment_id}", response_model=BaseResponse, summary="댓글 삭제")
async def delete_comment(comment_id: int, password: str, service: CommentService = Depends(get_comment_service)):
    service.delete_comment(comment_id, password)
    return BaseResponse(message="댓글이 삭제되었습니다.")

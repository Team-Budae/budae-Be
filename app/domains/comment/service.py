from app.common.exceptions import ForbiddenError, NotFoundError
from app.domains.comment.models import Comment
from app.domains.comment.repository import CommentRepository
from app.domains.comment.schemas import CommentCreate, CommentUpdate
from app.domains.post.models import Post


class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def list_comments(self, post_id: int) -> list[Comment]:
        return self.repository.list_by_post(post_id)

    def create_comment(self, payload: CommentCreate) -> Comment:
        post = self.repository.session.get(Post, payload.post_id)
        if not post or post.is_deleted:
            raise NotFoundError("게시글을 찾을 수 없습니다.")

        comment = Comment(**payload.model_dump())
        self.repository.session.add(comment)
        post.comments = (post.comments or 0) + 1
        self.repository.session.commit()
        self.repository.session.refresh(comment)
        return comment

    def update_comment(self, comment_id: int, payload: CommentUpdate) -> Comment:
        comment = self.repository.get_by_id(comment_id)
        if not comment or comment.is_deleted:
            raise NotFoundError("댓글을 찾을 수 없습니다.")
        if payload.password and comment.password != payload.password:
            raise ForbiddenError("비밀번호가 일치하지 않습니다.")
        if payload.content is not None:
            comment.content = payload.content
        self.repository.session.commit()
        self.repository.session.refresh(comment)
        return comment

    def delete_comment(self, comment_id: int, password: str) -> None:
        comment = self.repository.get_by_id(comment_id)
        if not comment or comment.is_deleted:
            raise NotFoundError("댓글을 찾을 수 없습니다.")
        if comment.password != password:
            raise ForbiddenError("비밀번호가 일치하지 않습니다.")
        comment.is_deleted = 1
        post = self.repository.session.get(Post, comment.post_id)
        if post and not post.is_deleted:
            post.comments = max((post.comments or 0) - 1, 0)
        self.repository.session.commit()

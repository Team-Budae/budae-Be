from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.domains.comment.models import Comment


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: Session):
        super().__init__(session, Comment)

    def list_by_post(self, post_id: int) -> list[Comment]:
        return (
            self.session.query(Comment)
            .filter(Comment.post_id == post_id, or_(Comment.is_deleted == 0, Comment.is_deleted.is_(None)))
            .all()
        )

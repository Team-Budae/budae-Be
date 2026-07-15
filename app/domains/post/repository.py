from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.domains.post.models import Post


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: Session):
        super().__init__(session, Post)

    def list_posts(self, *, skip: int = 0, limit: int = 20) -> tuple[list[Post], int]:
        query = self.session.query(Post).filter(Post.is_deleted == 0).order_by(Post.id.desc())
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

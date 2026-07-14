from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.domains.post.models import Post


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: Session):
        super().__init__(session, Post)

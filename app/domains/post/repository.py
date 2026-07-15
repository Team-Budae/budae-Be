from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.domains.comment.models import Comment
from app.domains.post.models import Post


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: Session):
        super().__init__(session, Post)

    def list_posts(self, *, skip: int = 0, limit: int = 20, sort: str = "latest") -> tuple[list[Post], int]:
        query = self.session.query(Post).filter(Post.is_deleted == 0)
        total = query.count()
        items = self._order_posts(query, sort).offset(skip).limit(limit).all()
        self._attach_comment_preview(items)
        return items, total

    def list_popular_posts(self, *, limit: int = 5) -> list[Post]:
        items = (
            self.session.query(Post)
            .filter(Post.is_deleted == 0)
            .order_by(Post.views.desc(), Post.id.desc())
            .limit(limit)
            .all()
        )
        self._attach_comment_preview(items)
        return items

    def _order_posts(self, query, sort: str):
        if sort == "popular":
            return query.order_by(Post.views.desc(), Post.id.desc())
        return query.order_by(Post.id.desc())

    def _attach_comment_preview(self, posts: list[Post]) -> None:
        post_ids = [post.id for post in posts]
        if not post_ids:
            return

        comments = (
            self.session.query(Comment)
            .filter(Comment.post_id.in_(post_ids), Comment.is_deleted == 0)
            .order_by(Comment.post_id.asc(), Comment.id.desc())
            .all()
        )
        preview_by_post_id: dict[int, list[Comment]] = {}

        for comment in comments:
            preview = preview_by_post_id.setdefault(comment.post_id, [])
            if len(preview) < 2:
                preview.append(comment)

        for post in posts:
            post.comment_preview = preview_by_post_id.get(post.id, [])

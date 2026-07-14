from app.common.exceptions import ForbiddenError, NotFoundError
from app.domains.post.models import Post
from app.domains.post.repository import PostRepository
from app.domains.post.schemas import PostCreate, PostUpdate


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def list_posts(self, *, skip: int = 0, limit: int = 20) -> list[Post]:
        return self.repository.list_all(skip=skip, limit=limit)

    def get_post(self, post_id: int) -> Post:
        post = self.repository.get_by_id(post_id)
        if not post or post.is_deleted:
            raise NotFoundError("게시글을 찾을 수 없습니다.")
        return post

    def create_post(self, payload: PostCreate) -> Post:
        post = Post(**payload.model_dump())
        return self.repository.add(post)

    def update_post(self, post_id: int, payload: PostUpdate) -> Post:
        post = self.get_post(post_id)
        if payload.password and post.password != payload.password:
            raise ForbiddenError("비밀번호가 일치하지 않습니다.")
        for key, value in payload.model_dump(exclude_unset=True, exclude={"password"}).items():
            setattr(post, key, value)
        self.repository.session.commit()
        self.repository.session.refresh(post)
        return post

    def delete_post(self, post_id: int, password: str) -> None:
        post = self.get_post(post_id)
        if post.password != password:
            raise ForbiddenError("비밀번호가 일치하지 않습니다.")
        post.is_deleted = 1
        self.repository.session.commit()

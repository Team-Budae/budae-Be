from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    post_id: int
    content: str | None = None
    author_name: str | None = None
    password: str | None = None


class CommentRead(CommentBase):
    id: int
    is_deleted: int = 0


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str | None = None
    password: str | None = None

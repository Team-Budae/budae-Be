from pydantic import BaseModel, ConfigDict, Field


class PostCommentPreview(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str | None = None
    author_name: str | None = None
    created_at: str | None = None


class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    place_id: int | None = None
    category: str | None = None
    title: str | None = None
    content: str | None = None
    author_name: str | None = None
    password: str | None = None


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    place_id: int | None = None
    category: str | None = None
    title: str | None = None
    content: str | None = None
    author_name: str | None = None
    is_deleted: int = 0
    views: int = 0
    likes: int = 0
    comments: int = 0
    comment_preview: list[PostCommentPreview] = Field(default_factory=list)
    date: str | None = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    place_id: int | None = None
    category: str | None = None
    title: str | None = None
    content: str | None = None
    author_name: str | None = None
    password: str | None = None
    views: int | None = None
    likes: int | None = None
    comments: int | None = None
    date: str | None = None


class PasswordVerify(BaseModel):
    password: str

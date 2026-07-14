from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    place_id: int | None = None
    category: str | None = None
    title: str | None = None
    content: str | None = None
    author_name: str | None = None
    password: str | None = None


class PostRead(PostBase):
    id: int
    is_deleted: int = 0


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    password: str | None = None

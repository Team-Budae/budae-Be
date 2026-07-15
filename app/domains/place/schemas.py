from pydantic import BaseModel, ConfigDict, Field


class PlaceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    content_type_id: int | None = None
    content_type_name: str | None = None
    addr1: str | None = None
    district_name: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    first_image_url: str | None = None
    thumbnail_url: str | None = None


class PlaceRead(PlaceBase):
    id: int
    content_id: str | None = None
    event_start_date: str | None = None
    event_end_date: str | None = None
    event_place: str | None = None


class PlaceCreate(PlaceBase):
    content_id: str | None = None


class PlaceUpdate(BaseModel):
    title: str | None = None
    addr1: str | None = None
    district_name: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    first_image_url: str | None = None
    thumbnail_url: str | None = None

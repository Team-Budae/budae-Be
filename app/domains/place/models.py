import json

from sqlalchemy import Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    content_type_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    content_type_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    addr1: Mapped[str | None] = mapped_column(Text, nullable=True)
    addr2: Mapped[str | None] = mapped_column(Text, nullable=True)
    district_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    first_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    def _raw_value(self, key: str) -> str | None:
        if not self.raw_json:
            return None

        try:
            payload = json.loads(self.raw_json)
        except json.JSONDecodeError:
            return None

        value = payload.get(key)
        if value in (None, "", " "):
            return None
        return str(value)

    @property
    def event_start_date(self) -> str | None:
        return self._raw_value("eventstartdate")

    @property
    def event_end_date(self) -> str | None:
        return self._raw_value("eventenddate")

    @property
    def event_place(self) -> str | None:
        return self._raw_value("eventplace")

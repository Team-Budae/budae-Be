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

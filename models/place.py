from sqlalchemy import Float, Integer, String, Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class Place(Base):
    __tablename__ = "places"

    # 내부 PK
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # 공공데이터 고유 ID
    content_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    # 관광지 / 숙박 / 축제 ...
    content_type_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    addr1: Mapped[str | None] = mapped_column(Text)

    addr2: Mapped[str | None] = mapped_column(Text)

    zipcode: Mapped[str | None] = mapped_column(String)

    tel: Mapped[str | None] = mapped_column(String)

    mapx: Mapped[float | None] = mapped_column(Float)

    mapy: Mapped[float | None] = mapped_column(Float)

    firstimage: Mapped[str | None] = mapped_column(Text)

    firstimage2: Mapped[str | None] = mapped_column(Text)

    createdtime: Mapped[str | None] = mapped_column(String)

    modifiedtime: Mapped[str | None] = mapped_column(String)
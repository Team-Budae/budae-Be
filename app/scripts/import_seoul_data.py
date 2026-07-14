import json
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.domains.place.models import Place


DATA_DIR = Path(__file__).resolve().parents[1] / ".." / "data" / "서울"


def _safe_float(value: Any) -> float | None:
    if value in (None, "", " "):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_str(value: Any) -> str | None:
    if value in (None, "", " "):
        return None
    return str(value)


def _district_name(addr1: str | None) -> str | None:
    if not addr1:
        return None
    for token in addr1.split():
        if token.endswith("구"):
            return token
    return None


def import_seoul_data() -> dict[str, int]:
    session: Session = SessionLocal()
    try:
        count = 0
        for json_path in sorted(DATA_DIR.glob("서울_*.json")):
            with json_path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)

            if payload.get("region") != "서울":
                continue

            content_type_id = int(payload.get("contentTypeId", 0))
            content_type_name = payload.get("contentType", "")

            for item in payload.get("items", []):
                content_id = _safe_str(item.get("contentid"))
                existing = session.scalar(
                    select(Place).where(Place.content_id == content_id, Place.content_type_id == content_type_id)
                )
                if existing:
                    continue

                place = Place(
                    content_id=content_id,
                    content_type_id=content_type_id,
                    content_type_name=content_type_name,
                    title=_safe_str(item.get("title")),
                    addr1=_safe_str(item.get("addr1")),
                    addr2=_safe_str(item.get("addr2")),
                    district_name=_district_name(_safe_str(item.get("addr1"))),
                    longitude=_safe_float(item.get("mapx")),
                    latitude=_safe_float(item.get("mapy")),
                    first_image_url=_safe_str(item.get("firstimage")),
                    thumbnail_url=_safe_str(item.get("firstimage2")),
                    raw_json=json.dumps(item, ensure_ascii=False),
                )
                session.add(place)
                count += 1

        session.commit()
        return {"imported": count}
    finally:
        session.close()


if __name__ == "__main__":
    result = import_seoul_data()
    print(result)

from app.common.exceptions import NotFoundError
from app.domains.place.models import Place
from app.domains.place.repository import PlaceRepository
from app.domains.place.schemas import PlaceCreate, PlaceUpdate


class PlaceService:
    def __init__(self, repository: PlaceRepository):
        self.repository = repository

    def get_places_list(self, keyword: str | None = None, content_type_id: int | None = None, *, skip: int = 0, limit: int = 20) -> tuple[list[Place], int]:
        return self.repository.search(keyword=keyword, content_type_id=content_type_id, skip=skip, limit=limit)

    def get_place(self, place_id: int) -> Place:
        place = self.repository.get_by_id(place_id)
        if not place:
            raise NotFoundError("장소를 찾을 수 없습니다.")
        return place

    def create_place(self, payload: PlaceCreate) -> Place:
        place = Place(**payload.model_dump())
        return self.repository.add(place)

    def update_place(self, place_id: int, payload: PlaceUpdate) -> Place:
        place = self.get_place(place_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(place, key, value)
        self.repository.session.commit()
        self.repository.session.refresh(place)
        return place

    def delete_place(self, place_id: int) -> None:
        place = self.get_place(place_id)
        self.repository.delete(place)

    

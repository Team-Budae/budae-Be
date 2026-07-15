from pydantic import BaseModel

from app.domains.place.schemas import PlaceRead


class DashboardTypeCounts(BaseModel):
    attraction: int = 0
    nature: int = 0
    accommodation: int = 0


class DashboardStats(BaseModel):
    place_count: int = 0
    festival_count: int = 0
    community_posts_count: int = 0
    type_counts: DashboardTypeCounts = DashboardTypeCounts()


class DashboardResponse(BaseModel):
    places: list[PlaceRead]
    festivals: list[PlaceRead]
    pins: list[PlaceRead]
    stats: DashboardStats

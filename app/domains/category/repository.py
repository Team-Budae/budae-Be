from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.domains.category.models import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: Session):
        super().__init__(session, Category)

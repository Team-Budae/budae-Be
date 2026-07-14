from app.common.exceptions import NotFoundError
from app.domains.category.models import Category
from app.domains.category.repository import CategoryRepository
from app.domains.category.schemas import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def list_categories(self, *, skip: int = 0, limit: int = 20) -> list[Category]:
        return self.repository.list_all(skip=skip, limit=limit)

    def get_category(self, category_id: int) -> Category:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise NotFoundError("카테고리를 찾을 수 없습니다.")
        return category

    def create_category(self, payload: CategoryCreate) -> Category:
        category = Category(**payload.model_dump())
        return self.repository.add(category)

    def update_category(self, category_id: int, payload: CategoryUpdate) -> Category:
        category = self.get_category(category_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        self.repository.session.commit()
        self.repository.session.refresh(category)
        return category

    def delete_category(self, category_id: int) -> None:
        category = self.get_category(category_id)
        self.repository.delete(category)

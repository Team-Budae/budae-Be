from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    """모든 리포지토리의 공통 베이스."""

    def __init__(self, session: Session, model_class: type[ModelT]):
        self.session = session
        self.model_class = model_class

    def get_by_id(self, entity_id: int) -> ModelT | None:
        return self.session.get(self.model_class, entity_id)

    def list_all(self, *, skip: int = 0, limit: int = 20) -> list[ModelT]:
        return self.session.query(self.model_class).offset(skip).limit(limit).all()

    def add(self, instance: ModelT) -> ModelT:
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def add_many(self, instances: list[ModelT]) -> list[ModelT]:
        self.session.add_all(instances)
        self.session.commit()
        for instance in instances:
            self.session.refresh(instance)
        return instances

    def delete(self, instance: ModelT) -> None:
        self.session.delete(instance)
        self.session.commit()

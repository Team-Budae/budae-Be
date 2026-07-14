from app.common.exceptions import NotFoundError
from app.domains.data_source.models import DataSource
from app.domains.data_source.repository import DataSourceRepository
from app.domains.data_source.schemas import DataSourceCreate, DataSourceUpdate


class DataSourceService:
    def __init__(self, repository: DataSourceRepository):
        self.repository = repository

    def list_data_sources(self, *, skip: int = 0, limit: int = 20) -> list[DataSource]:
        return self.repository.list_all(skip=skip, limit=limit)

    def get_data_source(self, data_source_id: int) -> DataSource:
        data_source = self.repository.get_by_id(data_source_id)
        if not data_source:
            raise NotFoundError("데이터 소스를 찾을 수 없습니다.")
        return data_source

    def create_data_source(self, payload: DataSourceCreate) -> DataSource:
        data_source = DataSource(**payload.model_dump())
        return self.repository.add(data_source)

    def update_data_source(self, data_source_id: int, payload: DataSourceUpdate) -> DataSource:
        data_source = self.get_data_source(data_source_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(data_source, key, value)
        self.repository.session.commit()
        self.repository.session.refresh(data_source)
        return data_source

    def delete_data_source(self, data_source_id: int) -> None:
        data_source = self.get_data_source(data_source_id)
        self.repository.delete(data_source)

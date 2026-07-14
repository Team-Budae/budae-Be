from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.domains.data_source.models import DataSource


class DataSourceRepository(BaseRepository[DataSource]):
    def __init__(self, session: Session):
        super().__init__(session, DataSource)

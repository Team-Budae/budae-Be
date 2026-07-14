from pydantic import BaseModel, ConfigDict


class DataSourceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    provider: str | None = None
    api_name: str | None = None
    source_url: str | None = None
    license_name: str | None = None
    attribution_text: str | None = None


class DataSourceRead(DataSourceBase):
    id: int


class DataSourceCreate(DataSourceBase):
    pass


class DataSourceUpdate(DataSourceBase):
    pass

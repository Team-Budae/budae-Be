from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.schemas import BaseResponse, PaginatedResponse
from app.core.database import get_db
from app.domains.data_source.repository import DataSourceRepository
from app.domains.data_source.schemas import DataSourceCreate, DataSourceRead, DataSourceUpdate
from app.domains.data_source.service import DataSourceService

router = APIRouter(prefix="/data-sources", tags=["data-sources"])


def get_data_source_service(db: Session = Depends(get_db)) -> DataSourceService:
    repository = DataSourceRepository(db)
    return DataSourceService(repository)


@router.get("", response_model=PaginatedResponse[DataSourceRead], summary="데이터 소스 목록 조회")
async def list_data_sources(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=10000),
    service: DataSourceService = Depends(get_data_source_service),
):
    items = service.list_data_sources(skip=skip, limit=limit)
    return {
        "items": [DataSourceRead.model_validate(item) for item in items],
        "pagination": {"page": (skip // limit) + 1 if limit else 1, "size": limit, "total": len(items)},
    }


@router.get("/{data_source_id}", response_model=DataSourceRead, summary="데이터 소스 상세 조회")
async def get_data_source(data_source_id: int, service: DataSourceService = Depends(get_data_source_service)):
    return DataSourceRead.model_validate(service.get_data_source(data_source_id))


@router.post("", response_model=DataSourceRead, status_code=status.HTTP_201_CREATED, summary="데이터 소스 생성")
async def create_data_source(payload: DataSourceCreate, service: DataSourceService = Depends(get_data_source_service)):
    data_source = service.create_data_source(payload)
    return DataSourceRead.model_validate(data_source)


@router.patch("/{data_source_id}", response_model=DataSourceRead, summary="데이터 소스 수정")
async def update_data_source(data_source_id: int, payload: DataSourceUpdate, service: DataSourceService = Depends(get_data_source_service)):
    data_source = service.update_data_source(data_source_id, payload)
    return DataSourceRead.model_validate(data_source)


@router.delete("/{data_source_id}", response_model=BaseResponse, summary="데이터 소스 삭제")
async def delete_data_source(data_source_id: int, service: DataSourceService = Depends(get_data_source_service)):
    service.delete_data_source(data_source_id)
    return BaseResponse(message="데이터 소스가 삭제되었습니다.")

from fastapi import APIRouter, Query, Depends
from app.core.database import get_database
from app.services.json_data_service import JsonDataService
from app.schemas.json_data import (
    JsonDataRequest,
    JsonDataResponse,
    ListResponse,
    LimitStatusResponse,
    HealthResponse,
    SetMaxUpdatesRequest
)
from databases import Database
from datetime import datetime


router = APIRouter()


def get_json_data_service(database: Database = Depends(get_database)) -> JsonDataService:
    """Dependency to get JSON data service."""
    return JsonDataService(database)


@router.post("/data", response_model=JsonDataResponse)
async def create_data(
    item: JsonDataRequest,
    service: JsonDataService = Depends(get_json_data_service)
):
    """Create new JSON data."""
    return await service.create_data(item)


@router.get("/data/{item_id}", response_model=JsonDataResponse)
async def get_data(
    item_id: str,
    service: JsonDataService = Depends(get_json_data_service)
):
    """Get JSON data by ID."""
    return await service.get_data(item_id)


@router.put("/data/{item_id}", response_model=JsonDataResponse)
async def update_data(
    item_id: str,
    item: JsonDataRequest,
    service: JsonDataService = Depends(get_json_data_service)
):
    """Update JSON data by ID."""
    return await service.update_data(item_id, item)    


@router.delete("/data/{item_id}")
async def delete_data(
    item_id: str,
    service: JsonDataService = Depends(get_json_data_service)
):
    """Delete JSON data by ID."""
    return await service.delete_data(item_id)


@router.get("/data", response_model=ListResponse)
async def list_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    service: JsonDataService = Depends(get_json_data_service)
):
    """List all stored data with pagination."""
    return await service.list_data(skip, limit)


@router.get("/data/{item_id}/limit-status", response_model=LimitStatusResponse)
async def get_limit_status(
    item_id: str,
    service: JsonDataService = Depends(get_json_data_service)
):
    """Get update limit status for a specific item."""
    return await service.get_limit_status(item_id)


@router.post("/data/{item_id}/reset-counter")
async def reset_update_counter(
    item_id: str,
    service: JsonDataService = Depends(get_json_data_service)
):
    """Reset update counter for a specific item."""
    return await service.reset_update_counter(item_id)


@router.post("/admin/data/{item_id}/set-max-updates")
async def set_max_updates(
    item_id: str,
    request: SetMaxUpdatesRequest,
    service: JsonDataService = Depends(get_json_data_service)
):
    """Set max updates for a specific item (Admin endpoint)."""
    return await service.set_max_updates(item_id, request.max_updates)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", timestamp=datetime.utcnow())

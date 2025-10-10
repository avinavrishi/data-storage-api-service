from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class JsonDataRequest(BaseModel):
    """Request model for JSON data."""
    data: Dict


class JsonDataResponse(BaseModel):
    """Response model for JSON data."""
    id: str
    data: Dict
    created_at: datetime
    last_updated: datetime
    limit_counter: int
    max_updates: int


class ListItem(BaseModel):
    """Model for list items."""
    id: str
    data: Dict
    created_at: datetime
    last_updated: datetime
    limit_counter: int
    max_updates: int


class ListResponse(BaseModel):
    """Response model for listing data."""
    total: int
    items: List[ListItem]


class LimitStatusResponse(BaseModel):
    """Response model for limit status."""
    id: str
    current_count: int
    max_updates: int
    remaining_updates: int
    can_update: bool


class UpdateLimitConfig(BaseModel):
    """Configuration model for update limits."""
    max_updates: int = Field(
        default=50, 
        ge=1, 
        le=1000, 
        description="Maximum number of updates allowed"
    )


class SetMaxUpdatesRequest(BaseModel):
    """Request model for setting max updates for a specific item."""
    max_updates: int = Field(ge=1, le=1000, description="Maximum number of updates allowed")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: datetime

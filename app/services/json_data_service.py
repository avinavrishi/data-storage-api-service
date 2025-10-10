import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from databases import Database
from sqlalchemy import Table, select, func

from app.core.database import json_store
from app.core.exceptions import UpdateLimitExceededException, ItemNotFoundException
from app.schemas.json_data import (
    JsonDataRequest, 
    JsonDataResponse, 
    ListItem, 
    ListResponse,
    LimitStatusResponse
)


class JsonDataService:
    """Service class for JSON data operations."""
    
    def __init__(self, database: Database):
        self.database = database
    
    async def create_data(self, item: JsonDataRequest) -> JsonDataResponse:
        """Create new JSON data."""
        item_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        query = json_store.insert().values(
            id=item_id,
            data=json.dumps(item.data),
            created_at=now,
            last_updated=now,
            limit_counter=0,
            max_updates=50  # Default max updates
        )
        await self.database.execute(query)
        
        # Return the created item
        created_item = await self.database.fetch_one(
            json_store.select().where(json_store.c.id == item_id)
        )
        
        return JsonDataResponse(
            id=created_item["id"],
            data=json.loads(created_item["data"]),
            created_at=created_item["created_at"],
            last_updated=created_item["last_updated"],
            limit_counter=created_item["limit_counter"],
            max_updates=created_item["max_updates"]
        )
    
    async def get_data(self, item_id: str) -> JsonDataResponse:
        """Get JSON data by ID."""
        query = json_store.select().where(json_store.c.id == item_id)
        row = await self.database.fetch_one(query)
        
        if not row:
            raise ItemNotFoundException(item_id)
        
        return JsonDataResponse(
            id=row["id"],
            data=json.loads(row["data"]),
            created_at=row["created_at"],
            last_updated=row["last_updated"],
            limit_counter=row["limit_counter"],
            max_updates=row["max_updates"]
        )
    
    async def update_data(
        self, 
        item_id: str, 
        item: JsonDataRequest
    ) -> JsonDataResponse:
        """Update JSON data by ID."""
        # First check if the item exists and get current limit_counter and max_updates
        existing_query = json_store.select().where(json_store.c.id == item_id)
        existing_row = await self.database.fetch_one(existing_query)
        
        if not existing_row:
            raise ItemNotFoundException(item_id)
        
        # Check if update limit is exceeded using the item's own max_updates
        if existing_row["limit_counter"] >= existing_row["max_updates"]:
            raise UpdateLimitExceededException(
                existing_row["limit_counter"], 
                existing_row["max_updates"]
            )
        
        # Update the data with incremented counter
        now = datetime.utcnow()
        update_query = json_store.update().where(json_store.c.id == item_id).values(
            data=json.dumps(item.data),
            last_updated=now,
            limit_counter=existing_row["limit_counter"] + 1
        )
        await self.database.execute(update_query)
        
        # Return the updated item
        updated_item = await self.database.fetch_one(
            json_store.select().where(json_store.c.id == item_id)
        )
        
        return JsonDataResponse(
            id=updated_item["id"],
            data=json.loads(updated_item["data"]),
            created_at=updated_item["created_at"],
            last_updated=updated_item["last_updated"],
            limit_counter=updated_item["limit_counter"],
            max_updates=updated_item["max_updates"]
        )
    
    async def delete_data(self, item_id: str) -> Dict[str, str]:
        """Delete JSON data by ID."""
        query = json_store.delete().where(json_store.c.id == item_id)
        result = await self.database.execute(query)
        
        if not result:
            raise ItemNotFoundException(item_id)
        
        return {"message": "Data deleted successfully", "id": item_id}
    
    async def list_data(self, skip: int = 0, limit: int = 10) -> ListResponse:
        """List all stored data with pagination."""
        # Total number of items
        total_query = select(func.count()).select_from(json_store)
        total_result = await self.database.fetch_one(total_query)
        total = total_result[0] if total_result else 0
        
        # Fetch items with pagination
        query = json_store.select().offset(skip).limit(limit)
        rows = await self.database.fetch_all(query)
        
        items = [
            ListItem(
                id=row["id"],
                data=json.loads(row["data"]),
                created_at=row["created_at"],
                last_updated=row["last_updated"],
                limit_counter=row["limit_counter"],
                max_updates=row["max_updates"]
            ) for row in rows
        ]
        
        return ListResponse(total=total, items=items)
    
    async def get_limit_status(self, item_id: str) -> LimitStatusResponse:
        """Get update limit status for a specific item."""
        query = json_store.select().where(json_store.c.id == item_id)
        row = await self.database.fetch_one(query)
        
        if not row:
            raise ItemNotFoundException(item_id)
        
        remaining_updates = row["max_updates"] - row["limit_counter"]
        
        return LimitStatusResponse(
            id=row["id"],
            current_count=row["limit_counter"],
            max_updates=row["max_updates"],
            remaining_updates=max(0, remaining_updates),
            can_update=row["limit_counter"] < row["max_updates"]
        )
    
    async def reset_update_counter(self, item_id: str) -> Dict[str, str]:
        """Reset update counter for a specific item."""
        query = json_store.select().where(json_store.c.id == item_id)
        row = await self.database.fetch_one(query)
        
        if not row:
            raise ItemNotFoundException(item_id)
        
        update_query = json_store.update().where(json_store.c.id == item_id).values(
            limit_counter=0,
            last_updated=datetime.utcnow()
        )
        await self.database.execute(update_query)
        
        return {"message": "Update counter reset successfully", "id": item_id}
    
    async def set_max_updates(self, item_id: str, max_updates: int) -> Dict[str, str]:
        """Set max updates for a specific item."""
        query = json_store.select().where(json_store.c.id == item_id)
        row = await self.database.fetch_one(query)
        
        if not row:
            raise ItemNotFoundException(item_id)
        
        update_query = json_store.update().where(json_store.c.id == item_id).values(
            max_updates=max_updates,
            last_updated=datetime.utcnow()
        )
        await self.database.execute(update_query)
        
        return {"message": f"Max updates set to {max_updates} successfully", "id": item_id}

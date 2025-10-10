from fastapi import HTTPException
from typing import Dict, Any


class UpdateLimitExceededException(HTTPException):
    """Exception raised when update limit is exceeded."""
    
    def __init__(self, current_count: int, max_updates: int):
        super().__init__(
            status_code=400,
            detail=f"Update limit exceeded. Maximum {max_updates} updates allowed. Current count: {current_count}"
        )


class ItemNotFoundException(HTTPException):
    """Exception raised when item is not found."""
    
    def __init__(self, item_id: str):
        super().__init__(
            status_code=404,
            detail=f"Item with ID '{item_id}' not found"
        )


class ValidationError(HTTPException):
    """Exception raised for validation errors."""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=detail
        )

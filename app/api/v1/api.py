from fastapi import APIRouter
from app.api.v1.endpoints import json_data

api_router = APIRouter()

api_router.include_router(json_data.router, tags=["json-data"])

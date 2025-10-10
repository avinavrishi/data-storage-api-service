import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_and_get_data():
    """Test creating and retrieving data."""
    # Create data
    test_data = {"name": "Test User", "age": 25}
    create_response = client.post("/api/v1/data", json={"data": test_data})
    assert create_response.status_code == 200
    
    item_id = create_response.json()["id"]
    
    # Get data
    get_response = client.get(f"/api/v1/data/{item_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"] == test_data
    assert get_response.json()["limit_counter"] == 0


def test_update_limit():
    """Test update limit functionality."""
    # Create data
    test_data = {"name": "Test User", "age": 25}
    create_response = client.post("/api/v1/data", json={"data": test_data})
    item_id = create_response.json()["id"]
    
    # Update data multiple times (should work within limit)
    updated_data = {"name": "Updated User", "age": 26}
    update_response = client.put(f"/api/v1/data/{item_id}", json={"data": updated_data})
    assert update_response.status_code == 200
    assert update_response.json()["limit_counter"] == 1
    
    # Check limit status
    limit_response = client.get(f"/api/v1/data/{item_id}/limit-status")
    assert limit_response.status_code == 200
    assert limit_response.json()["current_count"] == 1
    assert limit_response.json()["can_update"] == True

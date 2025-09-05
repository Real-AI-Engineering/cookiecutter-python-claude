{% if cookiecutter.project_type != "cli" -%}
"""Tests for items API endpoints."""

from __future__ import annotations

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestItemsAPI:
    """Test suite for items CRUD operations."""

    def test_list_items(self, client: TestClient) -> None:
        """Test listing all items."""
        response = client.get("/api/v1/items/")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        # Should have sample items from initialization
        assert len(data) > 0
        
        # Check structure of first item
        if data:
            item = data[0]
            assert "id" in item
            assert "name" in item
            assert "price" in item
            assert "created_at" in item
            assert "updated_at" in item

    def test_list_items_pagination(self, client: TestClient) -> None:
        """Test listing items with pagination."""
        # Test with skip
        response = client.get("/api/v1/items/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2

    def test_create_item(self, client: TestClient) -> None:
        """Test creating a new item."""
        item_data = {
            "name": "Test Item",
            "description": "This is a test item",
            "price": 99.99,
            "tax": 9.99,
        }
        
        response = client.post("/api/v1/items/", json=item_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["name"] == item_data["name"]
        assert data["description"] == item_data["description"]
        assert data["price"] == item_data["price"]
        assert data["tax"] == item_data["tax"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_item_validation(self, client: TestClient) -> None:
        """Test item creation with invalid data."""
        # Missing required field
        response = client.post("/api/v1/items/", json={"description": "No name"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Invalid price (negative)
        response = client.post(
            "/api/v1/items/",
            json={"name": "Test", "price": -10.00}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Invalid tax (negative)
        response = client.post(
            "/api/v1/items/",
            json={"name": "Test", "price": 10.00, "tax": -5.00}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_item(self, client: TestClient) -> None:
        """Test getting a single item."""
        # First create an item
        create_response = client.post(
            "/api/v1/items/",
            json={"name": "Get Test Item", "price": 49.99}
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        item_id = create_response.json()["id"]
        
        # Now get the item
        response = client.get(f"/api/v1/items/{item_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == "Get Test Item"
        assert data["price"] == 49.99

    def test_get_nonexistent_item(self, client: TestClient) -> None:
        """Test getting a non-existent item."""
        response = client.get("/api/v1/items/nonexistent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_update_item(self, client: TestClient) -> None:
        """Test updating an item."""
        # First create an item
        create_response = client.post(
            "/api/v1/items/",
            json={"name": "Update Test Item", "price": 29.99}
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        item_id = create_response.json()["id"]
        
        # Update the item
        update_data = {
            "name": "Updated Item",
            "description": "Now with description",
            "price": 39.99,
        }
        response = client.put(f"/api/v1/items/{item_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == "Updated Item"
        assert data["description"] == "Now with description"
        assert data["price"] == 39.99

    def test_partial_update_item(self, client: TestClient) -> None:
        """Test partial update of an item."""
        # First create an item
        create_response = client.post(
            "/api/v1/items/",
            json={
                "name": "Partial Update Test",
                "description": "Original description",
                "price": 19.99
            }
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        item_id = create_response.json()["id"]
        
        # Partial update - only change price
        response = client.put(f"/api/v1/items/{item_id}", json={"price": 24.99})
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["name"] == "Partial Update Test"  # Unchanged
        assert data["description"] == "Original description"  # Unchanged
        assert data["price"] == 24.99  # Updated

    def test_update_nonexistent_item(self, client: TestClient) -> None:
        """Test updating a non-existent item."""
        response = client.put(
            "/api/v1/items/nonexistent-id",
            json={"name": "New Name"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_item(self, client: TestClient) -> None:
        """Test deleting an item."""
        # First create an item
        create_response = client.post(
            "/api/v1/items/",
            json={"name": "Delete Test Item", "price": 9.99}
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        item_id = create_response.json()["id"]
        
        # Delete the item
        response = client.delete(f"/api/v1/items/{item_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert "deleted successfully" in data["message"]
        
        # Verify item is deleted
        get_response = client.get(f"/api/v1/items/{item_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_item(self, client: TestClient) -> None:
        """Test deleting a non-existent item."""
        response = client.delete("/api/v1/items/nonexistent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_search_items(self, client: TestClient) -> None:
        """Test searching items by name."""
        # Create items with specific names
        client.post(
            "/api/v1/items/",
            json={"name": "Search Test Alpha", "price": 10.00}
        )
        client.post(
            "/api/v1/items/",
            json={"name": "Search Test Beta", "price": 20.00}
        )
        client.post(
            "/api/v1/items/",
            json={"name": "Different Item", "price": 30.00}
        )
        
        # Search for "Search Test"
        response = client.get("/api/v1/items/search/?q=Search Test")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert len(data) >= 2
        for item in data:
            if item["name"] in ["Search Test Alpha", "Search Test Beta"]:
                assert "search test" in item["name"].lower()

    def test_search_items_case_insensitive(self, client: TestClient) -> None:
        """Test that search is case-insensitive."""
        # Create an item
        client.post(
            "/api/v1/items/",
            json={"name": "CaseSensitiveTest", "price": 15.00}
        )
        
        # Search with different cases
        for query in ["casesensitive", "CASESENSITIVE", "CaseSensitive"]:
            response = client.get(f"/api/v1/items/search/?q={query}")
            assert response.status_code == status.HTTP_200_OK
            
            data = response.json()
            found = any("casesensitive" in item["name"].lower() for item in data)
            assert found, f"Should find item with query '{query}'"

    def test_search_items_with_pagination(self, client: TestClient) -> None:
        """Test searching items with pagination."""
        response = client.get("/api/v1/items/search/?q=test&skip=0&limit=1")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert len(data) <= 1

    def test_search_items_empty_query(self, client: TestClient) -> None:
        """Test that empty search query returns validation error."""
        response = client.get("/api/v1/items/search/?q=")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_item_price_precision(self, client: TestClient) -> None:
        """Test that prices are rounded to 2 decimal places."""
        response = client.post(
            "/api/v1/items/",
            json={"name": "Precision Test", "price": 19.999, "tax": 1.999}
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["price"] == 20.00  # Should be rounded
        assert data["tax"] == 2.00  # Should be rounded
{% endif -%}
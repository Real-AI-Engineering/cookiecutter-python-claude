{% if cookiecutter.project_type != "cli" -%}
"""Items API endpoints - Example CRUD operations."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, status

from {{cookiecutter.project_slug}}.models.item import Item, ItemCreate, ItemUpdate
from {{cookiecutter.project_slug}}.services.item_service import ItemService

router = APIRouter()
item_service = ItemService()


@router.get(
    "/",
    response_model=list[Item],
    status_code=status.HTTP_200_OK,
    summary="List all items",
    description="Retrieve a list of all items with optional pagination",
)
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
) -> list[Item]:
    """
    List all items with pagination support.
    
    - **skip**: Number of items to skip (for pagination)
    - **limit**: Maximum number of items to return
    """
    return await item_service.get_items(skip=skip, limit=limit)


@router.post(
    "/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Create a new item with the provided data",
)
async def create_item(item: ItemCreate) -> Item:
    """
    Create a new item.
    
    - **name**: Item name (required)
    - **description**: Item description (optional)
    - **price**: Item price (must be positive)
    - **tax**: Tax amount (optional)
    """
    return await item_service.create_item(item)


@router.get(
    "/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK,
    summary="Get an item by ID",
    description="Retrieve a specific item by its ID",
)
async def get_item(item_id: str) -> Item:
    """
    Get a specific item by ID.
    
    - **item_id**: The unique identifier of the item
    """
    item = await item_service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{item_id}' not found",
        )
    return item


@router.put(
    "/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK,
    summary="Update an item",
    description="Update an existing item with new data",
)
async def update_item(item_id: str, item_update: ItemUpdate) -> Item:
    """
    Update an existing item.
    
    All fields are optional - only provided fields will be updated.
    
    - **item_id**: The unique identifier of the item
    - **name**: New item name
    - **description**: New item description
    - **price**: New item price
    - **tax**: New tax amount
    """
    item = await item_service.update_item(item_id, item_update)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{item_id}' not found",
        )
    return item


@router.delete(
    "/{item_id}",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Delete an item",
    description="Delete an item by its ID",
)
async def delete_item(item_id: str) -> dict[str, Any]:
    """
    Delete an item by ID.
    
    - **item_id**: The unique identifier of the item to delete
    """
    success = await item_service.delete_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{item_id}' not found",
        )
    return {"message": f"Item {item_id} deleted successfully"}


@router.get(
    "/search/",
    response_model=list[Item],
    status_code=status.HTTP_200_OK,
    summary="Search items",
    description="Search items by name",
)
async def search_items(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
) -> list[Item]:
    """
    Search items by name.
    
    - **q**: Search query (searches in item names)
    - **skip**: Number of items to skip (for pagination)
    - **limit**: Maximum number of items to return
    """
    return await item_service.search_items(query=q, skip=skip, limit=limit)
{% endif -%}
{% if cookiecutter.project_type != "cli" -%}
"""Item service - Example business logic layer."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from {{cookiecutter.project_slug}}.models.item import Item, ItemCreate, ItemUpdate
{% if cookiecutter.project_type != "cli" -%}
from {{cookiecutter.project_slug}}.core.logging import logger
{% else -%}
import logging

logger = logging.getLogger(__name__)
{% endif -%}


class ItemService:
    """
    Service class for item operations.
    
    This is an example implementation using in-memory storage.
    In a real application, this would interact with a database.
    """
    
    def __init__(self):
        """Initialize the service with in-memory storage."""
        self._items: dict[str, Item] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self) -> None:
        """Add some sample items for demonstration."""
        sample_items = [
            ItemCreate(
                name="Laptop",
                description="High-performance development laptop",
                price=1299.99,
                tax=129.99,
            ),
            ItemCreate(
                name="Mouse",
                description="Wireless ergonomic mouse",
                price=49.99,
                tax=5.00,
            ),
            ItemCreate(
                name="Keyboard",
                description="Mechanical keyboard with RGB lighting",
                price=149.99,
                tax=15.00,
            ),
        ]
        
        for item_data in sample_items:
            self.create_item_sync(item_data)
    
    async def get_items(self, skip: int = 0, limit: int = 100) -> list[Item]:
        """
        Get a list of items with pagination.
        
        Args:
            skip: Number of items to skip
            limit: Maximum number of items to return
            
        Returns:
            List of items
        """
        items = list(self._items.values())
        # Sort by created_at for consistent ordering
        items.sort(key=lambda x: x.created_at)
        
        logger.info("Fetching items", skip=skip, limit=limit, total=len(items))
        return items[skip : skip + limit]
    
    async def get_item(self, item_id: str) -> Optional[Item]:
        """
        Get a single item by ID.
        
        Args:
            item_id: The item's unique identifier
            
        Returns:
            The item if found, None otherwise
        """
        item = self._items.get(item_id)
        if item:
            logger.info("Item retrieved", item_id=item_id)
        else:
            logger.warning("Item not found", item_id=item_id)
        return item
    
    async def create_item(self, item_create: ItemCreate) -> Item:
        """
        Create a new item.
        
        Args:
            item_create: The item data
            
        Returns:
            The created item
        """
        return self.create_item_sync(item_create)
    
    def create_item_sync(self, item_create: ItemCreate) -> Item:
        """
        Synchronous version of create_item for internal use.
        
        Args:
            item_create: The item data
            
        Returns:
            The created item
        """
        now = datetime.now(timezone.utc)
        item = Item(
            id=f"item-{uuid.uuid4().hex[:8]}",
            **item_create.model_dump(),
            created_at=now,
            updated_at=now,
        )
        
        self._items[item.id] = item
        logger.info("Item created", item_id=item.id, item_name=item.name)
        return item
    
    async def update_item(
        self, item_id: str, item_update: ItemUpdate
    ) -> Optional[Item]:
        """
        Update an existing item.
        
        Args:
            item_id: The item's unique identifier
            item_update: The updated item data
            
        Returns:
            The updated item if found, None otherwise
        """
        existing_item = self._items.get(item_id)
        if not existing_item:
            logger.warning("Item not found for update", item_id=item_id)
            return None
        
        # Update only provided fields
        update_data = item_update.model_dump(exclude_unset=True)
        if update_data:
            for field, value in update_data.items():
                setattr(existing_item, field, value)
            existing_item.updated_at = datetime.now(timezone.utc)
            
            logger.info(
                "Item updated",
                item_id=item_id,
                updated_fields=list(update_data.keys()),
            )
        
        return existing_item
    
    async def delete_item(self, item_id: str) -> bool:
        """
        Delete an item.
        
        Args:
            item_id: The item's unique identifier
            
        Returns:
            True if the item was deleted, False if not found
        """
        if item_id in self._items:
            item = self._items.pop(item_id)
            logger.info("Item deleted", item_id=item_id, item_name=item.name)
            return True
        
        logger.warning("Item not found for deletion", item_id=item_id)
        return False
    
    async def search_items(
        self, query: str, skip: int = 0, limit: int = 100
    ) -> list[Item]:
        """
        Search items by name.
        
        Args:
            query: Search query (searches in item names, case-insensitive)
            skip: Number of items to skip
            limit: Maximum number of items to return
            
        Returns:
            List of matching items
        """
        query_lower = query.lower()
        matching_items = [
            item
            for item in self._items.values()
            if query_lower in item.name.lower()
        ]
        
        # Sort by created_at for consistent ordering
        matching_items.sort(key=lambda x: x.created_at)
        
        logger.info(
            "Items searched",
            query=query,
            matches=len(matching_items),
            skip=skip,
            limit=limit,
        )
        
        return matching_items[skip : skip + limit]
    
    async def get_item_count(self) -> int:
        """
        Get the total number of items.
        
        Returns:
            Total number of items
        """
        return len(self._items)


# Singleton instance for demonstration
# In a real application, this would be properly dependency-injected
_item_service_instance: Optional[ItemService] = None


def get_item_service() -> ItemService:
    """
    Get the singleton instance of ItemService.
    
    Returns:
        The ItemService instance
    """
    global _item_service_instance
    if _item_service_instance is None:
        _item_service_instance = ItemService()
    return _item_service_instance
{% endif -%}
{% if cookiecutter.project_type != "cli" -%}
"""Pydantic models for Item - Example data models."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ItemBase(BaseModel):
    """Base model for Item with common fields."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be positive)")
    tax: Optional[float] = Field(None, ge=0, description="Tax amount (optional)")
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        """Ensure price has at most 2 decimal places."""
        return round(v, 2)
    
    @field_validator("tax")
    @classmethod
    def validate_tax(cls, v: Optional[float]) -> Optional[float]:
        """Ensure tax has at most 2 decimal places."""
        if v is not None:
            return round(v, 2)
        return v


class ItemCreate(ItemBase):
    """Model for creating a new item."""
    
    pass


class ItemUpdate(BaseModel):
    """Model for updating an existing item - all fields optional."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    tax: Optional[float] = Field(None, ge=0)
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, v: Optional[float]) -> Optional[float]:
        """Ensure price has at most 2 decimal places."""
        if v is not None:
            return round(v, 2)
        return v
    
    @field_validator("tax")
    @classmethod
    def validate_tax(cls, v: Optional[float]) -> Optional[float]:
        """Ensure tax has at most 2 decimal places."""
        if v is not None:
            return round(v, 2)
        return v


class Item(ItemBase):
    """Complete Item model with all fields."""
    
    id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "item-123",
                "name": "Laptop",
                "description": "High-performance laptop for development",
                "price": 1299.99,
                "tax": 129.99,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z",
            }
        }
    }


# Example of additional models for different use cases
class ItemInDB(Item):
    """Model for Item as stored in database - can include internal fields."""
    
    is_deleted: bool = False
    version: int = 1


class ItemList(BaseModel):
    """Model for paginated list of items."""
    
    items: list[Item]
    total: int
    skip: int
    limit: int
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {
                        "id": "item-123",
                        "name": "Laptop",
                        "description": "High-performance laptop",
                        "price": 1299.99,
                        "tax": 129.99,
                        "created_at": "2024-01-01T12:00:00Z",
                        "updated_at": "2024-01-01T12:00:00Z",
                    }
                ],
                "total": 100,
                "skip": 0,
                "limit": 10,
            }
        }
    }
{% endif -%}
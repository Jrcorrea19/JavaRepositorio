from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from .models import AttentionPriority, TicketStatus


class ProductOut(BaseModel):
    id: int
    sku: str
    name: str
    price_ars: int
    stock: int

    class Config:
        from_attributes = True


class CommentIn(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120)
    message: str = Field(min_length=1, max_length=1000)


class CommentOut(BaseModel):
    id: int
    customer_name: str
    message: str
    product_name: str | None
    priority: AttentionPriority
    status: TicketStatus
    created_at: datetime

    class Config:
        from_attributes = True


class CommentStatusUpdate(BaseModel):
    status: TicketStatus

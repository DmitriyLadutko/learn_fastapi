from pydantic import BaseModel, Field
from datetime import datetime


class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    is_paid: bool = False


class OrderUpdate(BaseModel):
    product_name: str | None = None
    quantity: int | None = Field(None, gt=0)
    price: float | None = Field(None, gt=0)
    is_paid: bool | None = None


class OrderPublic(BaseModel):
    id: int
    user_id: int
    product_name: str
    quantity: int
    price: float
    is_paid: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

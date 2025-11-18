from pydantic import BaseModel, EmailStr, field_validator
from typing import List
from src.schemas.order import OrderPublic


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, v):
        if len(v) <= 3:
            raise ValueError("Name must be more than 3 symbols")
        return v


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None


class UserInDB(UserBase):
    id: int
    is_active: bool = True
    orders: List[OrderPublic] = []

    model_config = {"from_attributes": True}

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.db.session import get_db
from src.models.user import User
from src.schemas.order import OrderCreate, OrderUpdate, OrderPublic
from src.core.security import get_current_user
from src.crud.order import (
    get_order_by_id,
    get_orders,
    get_my_orders,
    create_order as crud_create_order,
    update_order as crud_update_order,
    delete_order as crud_delete_order,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/me", response_model=List[OrderPublic])
async def read_my_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    my_orders = await get_my_orders(db, current_user)
    return my_orders


@router.get("/", response_model=List[OrderPublic])
async def read_all_orders(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1),
        db: AsyncSession = Depends(get_db),
):
    return await get_orders(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderPublic)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderPublic.model_validate(order)


@router.put("/{order_id}", response_model=OrderPublic)
async def update_order_endpoint(order_id: int, order_in: OrderUpdate, db: AsyncSession = Depends(get_db)):
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await crud_update_order(db, order, order_in)
    return OrderPublic.model_validate(updated_order)


@router.post("/", response_model=OrderPublic, status_code=status.HTTP_201_CREATED)
async def create_order_endpoint(
        order_in: OrderCreate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    order_data = order_in.model_dump()
    order_data["user_id"] = current_user.id
    new_order = await crud_create_order(db, OrderCreate(**order_data))
    return OrderPublic.model_validate(new_order)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_endpoint(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await crud_delete_order(db, order)

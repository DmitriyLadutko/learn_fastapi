from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.order import Order
from src.schemas.order import OrderCreate, OrderUpdate
from src.core.security import get_current_user


async def get_my_orders(db: AsyncSession, current_user: get_current_user):
    result = await db.execute(select(Order).where(Order.user_id == current_user.id))
    return result.scalar_one_or_none()

async def get_order_by_id(db: AsyncSession, order_id: int) -> Order | None:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def get_orders(db: AsyncSession, skip: int, limit: int) -> Sequence[Order]:
    result = await db.execute(select(Order).offset(skip).limit(limit))
    return result.scalars().all()


async def create_order(db: AsyncSession, order_in: OrderCreate) -> Order:
    new_order = Order(**order_in.model_dump())
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order


async def update_order(db: AsyncSession, order: Order, order_in: OrderUpdate) -> Order:
    update_data = order_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)

    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def delete_order(db: AsyncSession, order: Order) -> None:
    await db.delete(order)
    await db.commit()

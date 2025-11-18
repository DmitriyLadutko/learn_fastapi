from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.models.user import User
from src.db.session import get_db
from src.core.security import get_current_user, get_password_hash
from src.schemas.user import UserInDB, UserUpdate
from src.crud.user import (
    get_user_by_id,
    get_user_by_email,
    get_all_users,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(path="/me", response_model=UserInDB)
async def read_my_profile(current_user: User = Depends(get_current_user)):
    return UserInDB.model_validate(current_user)


@router.get(path="/{user_id}", response_model=UserInDB)
async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_user)
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInDB.model_validate(user)


@router.get(path="/by-email/{email}", response_model=UserInDB)
async def get_user_by_email_route(
        email: str,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_user)
):
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInDB.model_validate(user)


@router.get("/", response_model=List[UserInDB])
async def list_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_user)
):
    users = await get_all_users(db, skip=skip, limit=limit)
    return users


@router.patch("/{user_id}", response_model=UserInDB)
async def update_user_route(
        user_id: int,
        user_in: UserUpdate,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_user)
):
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    updated = await update_user(db, user_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInDB.model_validate(updated)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_user)
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await delete_user(db, user)

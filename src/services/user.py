from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserCreate, UserInDB
from src.crud.user import get_user_by_email, create_user
from src.core.security import get_password_hash


async def create_user_service(db: AsyncSession, user_in: UserCreate) -> UserInDB:
    if await get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(user_in.password)
    db_user = await create_user(db, user_in, hashed)
    return UserInDB.model_validate(db_user)

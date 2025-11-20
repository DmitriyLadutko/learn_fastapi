from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.base import Base
from src.db.session import engine
from src.api.v1 import auth, users, orders
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.models.user import User
    from src.models.order import Order
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="FastAPI test",
    lifespan=lifespan,
    docs_url="/docs",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    return {"message": "API готово! /docs → Swagger"}


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )

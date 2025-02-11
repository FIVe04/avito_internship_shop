from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import init_db, cleanup_db
from app.core.dependencies import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await cleanup_db()


app = FastAPI(title="AvitoShop", version="1.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"Hello": "World"}








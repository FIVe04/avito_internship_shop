from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.database import init_db, cleanup_db, async_session_maker
from app.core.dependencies import get_db

from app.crud.product import add_products_to_db
from app.routers.auth import router as auth_router
from app.routers.purchase import router as purchase_router
from app.routers.transaction import router as transaction_router
from app.routers.info import router as info_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    async with async_session_maker() as session:
        await add_products_to_db(session)

    yield

    await cleanup_db()


app = FastAPI(title="AvitoShop", version="1.0", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Неверный запрос."},
    )

app.include_router(auth_router)
app.include_router(purchase_router)
app.include_router(transaction_router)
app.include_router(info_router)









from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, AsyncTransaction, AsyncSession

from app.core.dependencies import get_db
from app.crud.product import add_products_to_db
from app.main import app
from tests.settings import settings


pytestmark = pytest.mark.anyio

engine = create_async_engine(settings.TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def connection(anyio_backend) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        async with engine.begin() as conn:
            from app.models.user import User
            from app.models.product import Product
            from app.models.inventory import Inventory
            from app.models.transaction import Transaction
            from app.core.database import Base
            await conn.run_sync(Base.metadata.create_all)

        async with AsyncSession(bind=connection) as session:
            await add_products_to_db(session)

        yield connection



@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction


@pytest.fixture()
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
        expire_on_commit=False
    )

    yield async_session

    await transaction.rollback()


@pytest.fixture()
async def client(
        connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False
        )
        async with async_session:
            yield async_session

    app.dependency_overrides[get_db] = override_get_async_session
    yield AsyncClient(app=app, base_url="http://test")
    del app.dependency_overrides[get_db]

    await transaction.rollback()
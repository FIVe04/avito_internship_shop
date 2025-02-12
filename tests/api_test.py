from typing import AsyncGenerator
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, AsyncTransaction, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.dependencies import get_db
from app.main import app

pytestmark = pytest.mark.anyio


engine = create_async_engine("postgresql+asyncpg://ivanfrolov:Ivan07051978@localhost:5432/avito_test")


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
    )

    yield async_session

    await transaction.rollback()


# async def test_create_profile(session: AsyncSession):
#     existing_profiles = (await session.execute(select(Profile))).scalars().all()
#     assert len(existing_profiles) == 0
#
#     test_name = "test"
#     session.add(Profile(name=test_name))
#     await session.commit()
#
#     existing_profiles = (await session.execute(select(Profile))).scalars().all()
#     assert len(existing_profiles) == 1
#     assert existing_profiles[0].name == test_name


# async def test_rollbacks_between_functions(session: AsyncSession):
#     existing_profiles = (await session.execute(select(Profile))).scalars().all()
#     assert len(existing_profiles) == 0


@pytest.fixture()
async def client(
        connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
        async with async_session:
            yield async_session

    # Here you have to override the dependency that is used in FastAPI's
    # endpoints to get SQLAlchemy's AsyncSession. In my case, it is
    # get_async_session
    app.dependency_overrides[get_db] = override_get_async_session
    yield AsyncClient(app=app, base_url="http://test")
    del app.dependency_overrides[get_db]

    await transaction.rollback()


async def test_api_create_profile(client: AsyncClient):
    test_name = "test"
    async with client as ac:
        response = await ac.post(
            "/api/auth/",
            data={"username": "testNew", "password": "passwd"},
        )


        assert response.status_code == 200
        assert response.json().get('access_token') is not None




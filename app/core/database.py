from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, sessionmaker

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


async def init_db():
    async with engine.begin() as conn:
        from app.models.user import User
        from app.models.product import Product
        from app.models.inventory import Inventory
        from app.models.transaction import Transaction
        await conn.run_sync(Base.metadata.create_all)



async def cleanup_db():
    await engine.dispose()
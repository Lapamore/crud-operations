import os
from typing import AsyncGenerator

from dishka import Provider, provide, Scope
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class SessionProvider(Provider):

    @provide(scope=Scope.APP)
    def get_async_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        postgres_dsn: URL = URL.create(
            drivername="postgresql+asyncpg",
            username=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASS"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DATABASE"),
        )
        engine = create_async_engine(url=postgres_dsn)
        return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

import asyncpg
from typing import AsyncGenerator
from app.config import settings

# Global connection pool
_pool = None

async def create_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            user=settings.PGUSER,
            password=settings.PGPASSWORD,
            database=settings.PGDATABASE,
            host=settings.PGHOST,
            port=settings.PGPORT,
            min_size=1,
            max_size=10
        )
    return _pool

async def close_pool():
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None

async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """Dependency to get a connection from the pool."""
    pool = await create_pool()
    async with pool.acquire() as connection:
        yield connection

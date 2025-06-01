import asyncpg
from asyncpg import Pool
import db.settings as conf

pool: Pool = None


async def startup_db():
    global pool
    pool = await asyncpg.create_pool(conf.DB_URL, min_size=5, max_size=20)


async def shutdown_db():
    await pool.close()


async def get_db():
    async with pool.acquire() as connection:
        yield connection

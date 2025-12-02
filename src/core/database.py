import asyncpg
from src.core.config import settings


class Database:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            ssl="require",
            min_size=1,
            max_size=10,
        )

    async def get_connection(self):
        if self.pool is None:
            raise RuntimeError("Pool not initialized. Call create_pool() first.")
        return await self.pool.acquire()

    async def release_connection(self, conn):
        if self.pool is None:
            raise RuntimeError("Pool not initialized.")
        await self.pool.release(conn)

    async def execute_query(self, query: str, params=None):
        conn = await self.get_connection()
        try:
            result = await conn.fetch(query, *params) if params else await conn.fetch(query)
            return [dict(record) for record in result]
        finally:
            await self.release_connection(conn)

    async def execute_insert(self, query: str, params=None):
        conn = await self.get_connection()
        try:
            row = await conn.fetchrow(query, *params) if params else await conn.fetchrow(query)
            # Return PostgreSQL generated id if available
            print(row)
            return row["id"] if row and "id" in row else None
        finally:
            await self.release_connection(conn)

    async def execute_update(self, query: str, params=None):
        conn = await self.get_connection()
        try:
            result = await conn.execute(query, *params) if params else await conn.execute(query)
            # result looks like 'UPDATE <number>'
            return int(result.split()[-1])
        finally:
            await self.release_connection(conn)

    async def connection(self):
        conn = await self.get_connection()
        try:
            yield conn
        finally:
            await self.release_connection(conn)

    async def close(self):
        if self.pool:
            await self.pool.close()


db = Database()















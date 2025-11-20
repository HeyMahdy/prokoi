from pymysql.cursors import DictCursor
from src.core.config import settings
import aiomysql

class Database:
    def __init__(self):
      self.pool = None

    async def create_pool(self):
      self.pool = await aiomysql.create_pool(
       host=settings.DB_HOST,
       user=settings.DB_USER,
       password=settings.DB_PASSWORD,
       port =  settings.DB_PORT,
        db  = settings.DB_NAME,
          cursorclass=DictCursor,
          autocommit=True,
          minsize=1,
          maxsize=10

      )
    async def get_connection(self):
        if self.pool is None:
            raise RuntimeError("Pool not initialized. Call create_pool() first.")
        return await self.pool.acquire()

    async def release_connection(self, conn):
        if self.pool is None:
            raise RuntimeError("Pool not initialized.")
        self.pool.release(conn)

    async def execute_query(self, query:str,params=None):
      conn = await self.get_connection()
      try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query,params)
            await conn.commit()
            result = await cursor.fetchall()
            print("inside the repo")
            print(result)
            return result
      finally:
          await self.release_connection(conn)



    async def execute_insert(self,query:str,params=None):
        conn = await self.get_connection()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                await conn.commit()
                user_id = cursor.lastrowid
                return user_id
        finally:
            await self.release_connection(conn)



    async def execute_update(self,query:str,params=None):
        conn = await self.get_connection()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                await conn.commit()
                result = cursor.rowcount
                return result

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
            self.pool.close()





db = Database()















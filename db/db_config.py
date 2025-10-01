from asyncpg.pool import Pool
from asyncpg import create_pool, Record
from app.const import (
    LOCALHOST_ADDRESS,
    SUCCESS_CLOSE_POOL_MESSAGE,
    POOL_DOESNT_EXIST_OR_CLOSED
)
from app.config import DbLogger

class DbMaster:
    def __init__(self, pool: Pool) -> None:
        self.pool = pool
    
    @staticmethod
    async def create_pool(dsn: str) -> "DbMaster":
        
        pool = await create_pool(
            dsn=dsn,
            min_size=3,
            max_size=25,
            timeout=30,
            command_timeout=30
        )

        return DbMaster(pool)
    
    async def close_pool(self) -> None:
        if self.pool:
            await self.pool.close()
            await self.__do_info_log(SUCCESS_CLOSE_POOL_MESSAGE)
        else:
            await self.__do_warning_log(POOL_DOESNT_EXIST_OR_CLOSED)
    
    async def get_data_from_db(self, query: str, get_one_row_flag: bool = False, *args) -> list[Record] | Record | None: ## Запросы возвращающие данные: SELECT, ... 
        async with self.pool.acquire() as conn:
            try:
                if get_one_row_flag: #? Одна строка требуется только
                    return await conn.fetchone(query, *args)
                return await conn.fetch(query, *args)
            except Exception as e:
               await self.__do_error_log(e)
        
    async def execute_query(self, query: str, args: tuple) -> None: ## Запросы не возвращающие данных: UPDATE, INSERT, ... 
        async with self.pool.acquire() as conn:
            try:
                if len(args) == 0: ## Если один аргументов нет, то используем execute без args
                    await conn.execute(query)
                elif len(args) == 1:
                    await conn.execute(query, *args) ## Если один аргумент, используем execute
                else:
                    await conn.executemany(query, args)
            except Exception as e:
                await self.__do_error_log(e)

    
    @staticmethod
    async def __do_error_log(exception: Exception) -> None:
        DbLogger.error(f"{exception.__class__}: {exception}")

    @staticmethod
    async def __do_info_log(message: str) -> None:
        DbLogger.info(message)
    
    @staticmethod
    async def __do_warning_log(message: str) -> None:
        DbLogger.warning(message)



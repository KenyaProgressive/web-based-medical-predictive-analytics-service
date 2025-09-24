from asyncpg.pool import Pool
from asyncpg import create_pool, Record
from app.const import (
    LOCALHOST_ADDRESS,
    SUCCESS_CLOSE_POOL_MESSAGE,
    POOL_DOESNT_EXIST_OR_CLOSED
)
from app.config import DbLogger

class DbMaster:
    async def __init__(self, 
                 username: str, 
                 password: str, 
                 host: str = LOCALHOST_ADDRESS, 
                 port: int = 5432,
                 max_connections: int = 25) -> None:
        
        self.pool: Pool = await create_pool(
            user=username,
            password=password,
            host=host,
            port=port,
            min_size=3,
            max_size=max_connections,
            max_queries=1000,
            max_inactive_connection_lifetime=300,
            timeout=30,
            command_timeout=30
        )
    
    async def close_pool(self) -> None:
        if self.pool:
            await self.pool.close()
            self.__do_info_log(SUCCESS_CLOSE_POOL_MESSAGE)
        else:
            self.__do_warning_log(POOL_DOESNT_EXIST_OR_CLOSED)
    
    async def get_data_from_db(self, query: str, get_one_row_flag: bool = False, *args) -> list[Record] | Record | None: ## Запросы возвращающие данные: SELECT, ... 
        async with self.pool.acquire() as conn:
            try:
                if get_one_row_flag: #? Одна строка требуется только
                    return await conn.fetchone(query, *args)
                return await conn.fetch(query, *args)
            except Exception as e:
               self.__do_error_log(e)
        
    async def execute_query(self, query: str, *args) -> None: ## Запросы не возвращающие данных: UPDATE, INSERT, ... 
        async with self.pool.acquire() as conn:
            try:
                if len(args) == 1: ## Если один аргумент, то используем execute
                    await conn.execute(query, *args)
                else:
                    await conn.executemany(query, *args)
            except Exception as e:
                self.__do_error_log(e)

    
    @staticmethod
    async def __do_error_log(exception: Exception) -> None:
        DbLogger.error(f"{exception.__class__}: {exception}")
    
    @staticmethod
    async def __do_info_log(message: str) -> None:
        DbLogger.info(message)
    
    @staticmethod
    async def __do_warning_log(message: str) -> None:
        DbLogger.warning(message)



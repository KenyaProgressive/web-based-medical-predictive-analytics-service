import asyncio
import uvicorn
from db.query import CREATE_TABLE_BPM, CREATE_TABLE_UTERUS
from db.db_config import DbMaster
from app.const import (
    DB_CONNECTION_LINK, 
    NO_ARGS,
    LOCALHOST_ADDRESS,
    PORT,
    APP_PATH,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    DB_PORT,
    CSV_PATH_1,
    CSV_PATH_2,
)
from app.emulator.emulator import AsyncDualFolderEmulator
from app.config import CommonLogger


async def main():

    db_master: DbMaster = await DbMaster.create_pool(       
        dsn=DB_CONNECTION_LINK
    )

    try:
        await db_master.execute_query(CREATE_TABLE_BPM, NO_ARGS)
        await db_master.execute_query(CREATE_TABLE_UTERUS, NO_ARGS)
        # print("SUCCESS")
    except Exception as e:
        CommonLogger.error(e)

    
    emulator = AsyncDualFolderEmulator(
        folder1=CSV_PATH_1,
        folder2=CSV_PATH_2,
        delay=0.25,
        db_config={
            "user": POSTGRES_USER,
            "password": POSTGRES_PASSWORD,
            "database": POSTGRES_DB,
            "host": LOCALHOST_ADDRESS,
            "port": DB_PORT
        }
    )

    await emulator.stream_data_async()

   

    # uvicorn.run(APP_PATH, host=LOCALHOST_ADDRESS, port=PORT, reload=True)

    

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import uvicorn
from db.query import CREATE_TABLE_PARAMETRES
from db.db_config import DbMaster
from app.const import (
    DB_CONNECTION_LINK, 
    NO_ARGS,
    LOCALHOST_ADDRESS,
    PORT,
    APP_PATH
)
from app.config import CommonLogger


async def main():

    db_master: DbMaster = await DbMaster.create_pool(       
        dsn=DB_CONNECTION_LINK
    )

    try:
        await db_master.execute_query(CREATE_TABLE_PARAMETRES, NO_ARGS)
        print("SUCCESS")
    except Exception as e:
        CommonLogger.error(e)

    uvicorn.run(APP_PATH, host=LOCALHOST_ADDRESS, port=PORT, reload=True)

if __name__ == "__main__":
    asyncio.run(main())
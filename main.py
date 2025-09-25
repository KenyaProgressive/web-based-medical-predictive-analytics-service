from db.query import CREATE_TABLE_PARAMETRES
from db.db_config import DbMaster
from app.const import DB_CONNECTION_LINK, NO_ARGS

from app.config import CommonLogger
import asyncio

async def main():

    db_master: DbMaster = await DbMaster.create_pool(       
        dsn=DB_CONNECTION_LINK
    )

    try:
        await db_master.execute_query(CREATE_TABLE_PARAMETRES, NO_ARGS)
        print("SUCCESS")
    except Exception as e:
        CommonLogger.error(e)


if __name__ == "__main__":
    asyncio.run(main())
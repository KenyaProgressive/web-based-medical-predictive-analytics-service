import asyncio
import uvicorn
from db.query import CREATE_TABLE_HYPOXIA
from db.query import CREATE_TABLE_REGULAR
from db.db_config import DbMaster
from app.const import (
    DB_CONNECTION_LINK,
    NO_ARGS,
    LOCALHOST_ADDRESS,
    PORT,
    APP_PATH
)

from app.config import CommonLogger

from app.emulator.emulator import AsyncFileEmulator  # импортируйте ваш эмулятор здесь


async def main():

    db_master: DbMaster = await DbMaster.create_pool(
        dsn=DB_CONNECTION_LINK
    )

    try:
        await db_master.execute_query(CREATE_TABLE_HYPOXIA, NO_ARGS)
        await db_master.execute_query(CREATE_TABLE_REGULAR, NO_ARGS)
        print("SUCCESS")
    except Exception as e:
        CommonLogger.error(e)

    # Создаём и запускаем эмулятор
    emulator = AsyncFileEmulator(
        bpm_file='app/emulator/bpm.csv',
        uterus_file='app/emulator/uterus.csv',
        db_master=db_master,
        chunk_size=2,
        delay=1.0,
    )

    # Запускаем эмулятор как отдельную задачу вместе с сервером
    emulator_task = asyncio.create_task(emulator.stream_data_async())

    # Настраиваем uvicorn сервер
    config = uvicorn.Config(
        APP_PATH, 
        host=LOCALHOST_ADDRESS,
        port=PORT,
        reload=True
    )
    server = uvicorn.Server(config)

    # Запускаем сервер (await, чтобы не блокировать event loop)
    await server.serve()

    # Если сервер остановится, отменяем эмулятор
    emulator_task.cancel()
    try:
        await emulator_task
    except asyncio.CancelledError:
        print("Эмулятор остановлен")

    # Закрываем пул
    await db_master.close_pool()


if __name__ == "__main__":
    asyncio.run(main())

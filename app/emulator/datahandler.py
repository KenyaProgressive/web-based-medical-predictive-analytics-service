import asyncio
from datetime import datetime, timedelta
from typing import List
from asyncpg import Record
import pandas as pd

from db.db_config import DbMaster
from app.ml.get_ctg_data import get_ctg_data

class DataHandler:
    def __init__(self, db_master: DbMaster, bpm_table: str, uterus_table: str, interval: float = 4.0) -> None:
        self.db_master = db_master
        self.bpm_table = bpm_table
        self.uterus_table = uterus_table
        self.interval = interval
        self.start_time = datetime.utcnow()  # запоминает время старта
        self._task: asyncio.Task = None
        self.__result = {}

    @property
    def result(self):
        return self.__result

    async def _fetch_recent_data(self, table_name: str, since_time: datetime) -> List[Record]:
        query = f"""SELECT * FROM {table_name} WHERE time >= $1 ORDER BY time;"""

        ago_30_minutes = 0
        if since_time > 1800:
            ago_30_minutes = since_time - 1800

        records = await self.db_master.get_data_from_db(query, False, (ago_30_minutes))
        return records or []

    async def _send_to_ml(self):
        now = datetime.utcnow()
        time_threshold = now - self.start_time
        float_timestamp = time_threshold.total_seconds()

        bpm_records = await self._fetch_recent_data(self.bpm_table, float_timestamp)
        uterus_records = await self._fetch_recent_data(self.uterus_table, float_timestamp)

        bpm_df = pd.DataFrame([{ 'time': r['time'], 'bpm': r['bpm']} for r in bpm_records])
        uterus_df = pd.DataFrame([{ 'time': r['time'], 'uterus': r['uterus']} for r in uterus_records])

        result = get_ctg_data(bpm_df=bpm_df, uterus_df=uterus_df)
        self.__result = result
        print(result)
        # Дальше делать с result что надо (лог, отправка и т.д.)

    async def _run_periodic(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            try:
                await self._send_to_ml()
            except Exception as e:
                print(f"Ошибка при отправке данных в ML: {e}")

    async def start(self) -> None:
        if self._task is None or self._task.done():
            self.start_time = datetime.utcnow()  # сбрасываем время старта при запуске
            self._task = asyncio.create_task(self._run_periodic())

    async def stop(self) -> None:
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                print("Задача остановлена.")

# пример использования:
# handler = DataHandler(db_master, bpm_table='bpm_table', uterus_table='uterus_table') или какие там таблицы
# handler.start()

# Программа продолжает работать, DataHandler в фоне собирает и анализирует данные

# При остановке:
# await handler.stop()
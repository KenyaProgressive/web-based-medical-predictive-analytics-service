import asyncio
from datetime import datetime, timedelta
from typing import List
from asyncpg import Record
import pandas as pd

from db_config import DbMaster
from app.ml.your_ctg_module import get_ctg_data  # поправить на верный модуль


class DataHandler:
    def __init__(self, db_master: DbMaster, bpm_table: str, uterus_table: str, interval: float = 4.0) -> None:
        self.db_master = db_master
        self.bpm_table = bpm_table
        self.uterus_table = uterus_table
        self.interval = interval
        self.start_time = datetime.utcnow()  # запоминает время старта
        self._task: asyncio.Task = None

    async def _fetch_recent_data(self, table_name: str, since_time: datetime) -> List[Record]:
        query = f"""
            SELECT * FROM {table_name}
            WHERE get_data_time >= $1
            ORDER BY get_data_time
        """
        records = await self.db_master.get_data_from_db(query, False, since_time)
        return records or []

    async def _send_to_ml(self):
        now = datetime.utcnow()
        time_threshold = max(self.start_time, now - timedelta(minutes=30))  # начало интервала для выборки

        bpm_records = await self._fetch_recent_data(self.bpm_table, time_threshold)
        uterus_records = await self._fetch_recent_data(self.uterus_table, time_threshold)

        bpm_df = pd.DataFrame([{ 'time': r['get_data_time'], 'bpm': r['bpm']} for r in bpm_records])
        uterus_df = pd.DataFrame([{ 'time': r['get_data_time'], 'uterus': r['uterus']} for r in uterus_records])

        result = get_ctg_data(bpm_df, uterus_df)
        # Дальше делать с result что надо (лог, отправка и т.д.)

    async def _run_periodic(self) -> None:
        while True:
            try:
                await self._send_to_ml()
            except Exception as e:
                print(f"Ошибка при отправке данных в ML: {e}")
            await asyncio.sleep(self.interval)

    def start(self) -> None:
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


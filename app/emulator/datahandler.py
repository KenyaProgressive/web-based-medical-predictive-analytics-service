import asyncio
from datetime import datetime, timedelta
from typing import List
from asyncpg import Record
from db_config import DbMaster 


class DataHandler:
    """
    Класс для периодического извлечения данных за последние 30 минут из базы данных
    и отправки их в машину обучения (ML).
    """

    def __init__(self, db_master: DbMaster, table_name: str, interval: float = 4.0) -> None:
        """
        :param db_master: Экземпляр класса DbMaster для работы с PostgreSQL
        :param table_name: Имя таблицы в БД для выборки данных
        :param interval: Интервал в секундах между проверками и отправкой данных
        """
        self.db_master = db_master
        self.table_name = table_name
        self.interval = interval
        self._task: asyncio.Task = None

    async def _fetch_recent_data(self) -> List[Record]:
        """
        Запрашивает данные последних 30 минут из таблицы.
        :return: Список записей из базы (asyncpg.Record)
        """
        time_threshold = datetime.utcnow() - timedelta(minutes=30)
        query = f"""
            SELECT * FROM {self.table_name}
            WHERE get_data_time >= $1
        """
        records = await self.db_master.get_data_from_db(query, False, time_threshold)
        return records or []

    async def _send_to_ml(self, records: List[Record]) -> None:
        """
        Моковый метод отправки данных в ML.
        Замените на реальную реализацию.
        """
        if not records:
            return
        # Пример: просто вывод в консоль
        print(f"Отправка {len(records)} записей в ML модель...")
        # Не допер куда именно отпралять данные, можно дописать чисто на созвоне 

    async def _run_periodic(self) -> None:
        """
        Основной метод, который запускает периодическую задачу:
        каждые interval секунд извлекать данные и отправлять их в ML.
        """
        while True:
            try:
                records = await self._fetch_recent_data()
                if records:
                    await self._send_to_ml(records)
                else:
                    print("Нет данных за последние 30 минут для отправки.")
            except Exception as e:
                print(f"Ошибка при отправке данных в ML: {e}")
            await asyncio.sleep(self.interval)

    def start(self) -> None:
        """
        Запускает периодическую задачу отправки данных.
        """
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._run_periodic())

    async def stop(self) -> None:
        """
        Останавливает периодическую задачу, если она запущена.
        """
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                print("Задача отправки данных в ML остановлена.")
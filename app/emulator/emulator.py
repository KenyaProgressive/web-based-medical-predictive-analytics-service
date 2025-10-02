import asyncio
import csv
import os

from typing import List, Optional, Dict, Any
from db.db_config import DbMaster  # Импорт нашего класса DbMaster


class AsyncFileEmulator:
    """
    Асинхронный эмулятор потоковой передачи данных из двух CSV-файлов
    с записью данных в PostgreSQL через класс DbMaster.

    Эмулятор последовательно читает записи из двух CSV-файлов,
    по одной записи за раз с задержкой delay,
    и асинхронно вставляет их в соответствующие таблицы базы данных.
    """

    def __init__(self,
                 file1: str,
                 file2: str,
                 db_master: DbMaster,
                 chunk_size: int = 1,
                 delay: float = 1.0) -> None:
        """
        Инициализация эмулятора.

        :param file1: Путь к первому CSV-файлу (данные hypoxia).
        :param file2: Путь ко второму CSV-файлу (данные regular).
        :param db_master: Инстанс класса DbMaster для работы с базой.
        :param chunk_size: Количество записей для отправки за один шаг.
        :param delay: Задержка в секундах между отправками данных.
        """
        self.file1 = file1
        self.file2 = file2
        self.db_master = db_master
        self.chunk_size = chunk_size
        self.delay = delay
        self.data1: List[Dict[str, Any]] = []
        self.data2: List[Dict[str, Any]] = []

    def _load_csv_from_file(self, filename: str) -> List[Dict[str, Any]]:
        """
        Загрузить данные из CSV-файла в список словарей.

        :param filename: Путь к CSV-файлу.
        :return: Список записей, где каждая запись - словарь колонок.
        """
        data: List[Dict[str, Any]] = []
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден")
            return data
        try:
            with open(filename, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
        except Exception as e:
            print(f"Ошибка чтения файла {filename}: {e}")
        return data

    def _load_data(self) -> None:
        """Загрузить данные из обоих CSV-файлов в память."""
        self.data1 = self._load_csv_from_file(self.file1)
        self.data2 = self._load_csv_from_file(self.file2)

    async def _insert_rows(self, table_name: str, rows: List[Dict[str, Any]]) -> None:
        """
        Асинхронно вставить записи в таблицу базы данных.

        :param table_name: Имя таблицы для вставки.
        :param rows: Список словарей с данными для вставки.
        """
        if not rows:
            return
        sql = f"""
            INSERT INTO {table_name} (time, bpm, uterus)
            VALUES ($1, $2, $3)
        """
        for row in rows:
            try:
                t = float(row.get('time', 0))
                b = float(row.get('bpm', 0))
                u = float(row.get('uterus', 0))
                await self.db_master.execute_query(sql, (t, b, u))
            except Exception as e:
                print(f"Ошибка вставки данных в {table_name}: {e}")

    async def stream_data_async(self) -> None:
        """
        Асинхронно запустить эмуляцию отправки данных из обоих файлов,
        с записью порций данных в базу с указанной задержкой.
        """
        self._load_data()
        idx1, idx2 = 0, 0
        len1, len2 = len(self.data1), len(self.data2)

        while idx1 < len1 or idx2 < len2:
            rows1: List[Dict[str, Any]] = []
            rows2: List[Dict[str, Any]] = []

            if idx1 < len1:
                rows1 = self.data1[idx1:idx1 + self.chunk_size]
                idx1 += self.chunk_size

            if idx2 < len2:
                rows2 = self.data2[idx2:idx2 + self.chunk_size]
                idx2 += self.chunk_size

            await self._insert_rows('bpm', rows1)
            await self._insert_rows('uterus', rows2)

            # print(f"Отправлено в hypoxia_table: {len(rows1)} строк")
            # print(f"Отправлено в regular_table: {len(rows2)} строк")
            print('---')

            await asyncio.sleep(self.delay)


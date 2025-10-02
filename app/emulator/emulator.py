import asyncio
import csv
import os
from typing import List, Dict, Any
from db.db_config import DbMaster



class AsyncFileEmulator:
    """
    Асинхронный эмулятор, который читает два CSV файла:
    bpm.csv и uterus.csv, и вставляет их данные в две таблицы:
    hypoxia_table и regular_table.
    
    Формат CSV:
    time_sec,value
    """

    def __init__(self,
                 bpm_file: str,
                 uterus_file: str,
                 db_master: DbMaster,
                 chunk_size: int = 1,
                 delay: float = 0.25) -> None:
        self.bpm_file = bpm_file
        self.uterus_file = uterus_file
        self.db_master = db_master
        self.chunk_size = chunk_size
        self.delay = delay
        self.bpm_data: List[Dict[str, Any]] = []
        self.uterus_data: List[Dict[str, Any]] = []

    def _load_csv(self, filename: str) -> List[Dict[str, Any]]:
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден")
            return []
        try:
            with open(filename, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"Ошибка чтения {filename}: {e}")
            return []

    def _load_data(self) -> None:
        self.bpm_data = self._load_csv(self.bpm_file)
        self.uterus_data = self._load_csv(self.uterus_file)

    async def _insert_rows(self, table_name: str, rows: List[Dict[str, Any]]) -> None:
        if not rows:
            return
        for row in rows:
            try:
                t = float(row.get('time_sec', row.get('time', 0)))  # время в секундах из CSV
                val = float(row.get('value', 0))
                # В таблице hypoxia_table и regular_table есть 3 поля:
                # time, bpm, uterus. Нам нужно заполнить данные:
                # Для bpm.csv: time = t, bpm = val, uterus = NULL
                # Для uterus.csv: time = t, bpm = NULL, uterus = val
                if table_name == 'bpm':
                    sql = f"INSERT INTO bpm(time, bpm) VALUES ($1, $2)"
                    await self.db_master.execute_query(sql, (t, val))
                else:
                    sql = f"INSERT INTO uterus(time, uterus) VALUES ($1, $2)"  
                    await self.db_master.execute_query(sql, (t, val))
            except Exception as e:
                print(f"Ошибка вставки в {table_name}: {e}")

    async def stream_data_async(self) -> None:
        self._load_data()
        idx_bpm, idx_uterus = 0, 0
        len_bpm, len_uterus = len(self.bpm_data), len(self.uterus_data)

        while idx_bpm < len_bpm or idx_uterus < len_uterus:
            bpm_chunk = []
            uterus_chunk = []

            if idx_bpm < len_bpm:
                bpm_chunk = self.bpm_data[idx_bpm:idx_bpm + self.chunk_size]
                idx_bpm += self.chunk_size

            if idx_uterus < len_uterus:
                uterus_chunk = self.uterus_data[idx_uterus:idx_uterus + self.chunk_size]
                idx_uterus += self.chunk_size

            await self._insert_rows('bpm', bpm_chunk)
            await self._insert_rows('uterus', uterus_chunk)

            # print(f"Отправлено в hypoxia_table: {len(rows1)} строк")
            # print(f"Отправлено в regular_table: {len(rows2)} строк")
            print('---')

            await asyncio.sleep(self.delay)

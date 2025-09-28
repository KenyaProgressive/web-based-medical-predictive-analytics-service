import asyncio
import time
import csv
import os
import asyncpg
from datetime import time

class AsyncDualFolderEmulator:
    def __init__(self, folder1, folder2, chunk_size=1, delay=1.0, db_config=None):
        self.folder1 = folder1
        self.folder2 = folder2
        self.chunk_size = chunk_size
        self.delay = delay
        self.data1 = []
        self.data2 = []
        self.db_config = db_config or {}
        self.pool = None

    async def _init_db_pool(self):
        self.pool = await asyncpg.create_pool(**self.db_config)

    async def close(self):
        if self.pool:
            await self.pool.close()

    def _load_csv_from_file(self, filename):
        data = []
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


    def _load_data(self):
        self.data1 = self._load_csv_from_file(self.folder1)
        self.data2 = self._load_csv_from_file(self.folder2)

    async def _insert_rows(self, table_name, rows):
        if not rows or not self.pool:
            return
        sql = f"""
            INSERT INTO {table_name} (time, bpm, uterus)
            VALUES ($1, $2, $3)
        """
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for row in rows:
                    try:
                        t = float(row.get('time', 0))
                        b = float(row.get('bpm', 0))
                        u = float(row.get('uterus', 0))
                        await connection.execute(sql, t, b, u)
                    except Exception as e:
                        print(f"Ошибка вставки данных в {table_name}: {e}")

    async def stream_data_async(self):
        self._load_data()
        await self._init_db_pool()

        idx1, idx2 = 0, 0
        len1, len2 = len(self.data1), len(self.data2)

        while idx1 < len1 or idx2 < len2:
            rows1 = []
            rows2 = []

            if idx1 < len1:
                rows1 = self.data1[idx1:idx1 + self.chunk_size]
                idx1 += self.chunk_size

            if idx2 < len2:
                rows2 = self.data2[idx2:idx2 + self.chunk_size]
                idx2 += self.chunk_size

            await self._insert_rows('parametres', rows1)
            # await self._insert_rows('regular_table', rows2)

            print(f"Отправлено в hypoxia_table: {len(rows1)} строк")
            # print(f"Отправлено в regular_table: {len(rows2)} строк")
            print('---')

            await asyncio.sleep(self.delay)

        await self.close()

if __name__ == "__main__":
    db_config = {
        "user": "your_user",
        "password": "your_password",
        "database": "your_database",
        "host": "localhost",
        "port": 5433,
    }

    emulator = AsyncDualFolderEmulator(
        folder1='joined_data_hyp',
        folder2='joined_data_reg',
        chunk_size=1,
        delay=1.0,
        db_config=db_config
    )

    asyncio.run(emulator.stream_data_async())
#короче предполгается что в бд есть 2 таблицы hypoxia_table и 
#regular_table, оттуда данные и тянутся

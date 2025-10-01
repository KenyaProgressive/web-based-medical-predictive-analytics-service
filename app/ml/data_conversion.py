from typing import List
import pandas as pd

def join_data(files: List[str]) -> pd.DataFrame:
    """Функция для объединения файлов датасета в один файл с единым таймлайном"""
    united_df: pd.DataFrame = pd.DataFrame()

    time_since_beginning: float = 0
    for file in files:
        df: pd.DataFrame = pd.read_csv(file)
        df.rename(columns={'time_sec': 'time'}, inplace=True)

        df['time'] += time_since_beginning

        united_df = pd.concat([united_df, df], ignore_index=True)

        time_since_beginning = united_df['time'].max()

    return united_df

import pandas as pd

def join_data(files: list) -> pd.DataFrame:
    """Функция для объединения файлов датасета в один файл с единым таймлайном"""
    united_df = pd.DataFrame()

    time_since_beginning = 0
    for file in files:
        df = pd.read_csv(file)
        df['time_sec'] += time_since_beginning

        united_df = pd.concat([united_df, df], ignore_index=True)

        time_since_beginning = united_df['time_sec'].max()

    return united_df

import pandas as pd

def merging_time(data: pd.DataFrame):
    """
    Функция для объединения файлов датасета в один файл с единым таймлайном
    """

    time_since_beginning = 0
    for row in data.itertuples():
        if data.loc[row.Index, 'time_sec'] == 0 and row.Index > 0:
            time_since_beginning = data.loc[row.Index - 1, 'time_sec']

        data.loc[row.Index, 'time_sec'] += time_since_beginning

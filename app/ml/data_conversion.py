import pandas as pd
from typing import List, Dict, Union

def join_data(bpm_files: List[str], uterus_files: List[str]) -> pd.DataFrame:
    """
    Функция для объединения файлов датасета в один файл с единым таймлайном.
    
    Args:
        bpm_files: Список путей к csv-файлам с данными о ЧСС.
        uterus_files: Список путей к csv-файлам с данными о сокращениях матки.

    Returns:
        united_df: DataFrame со столбцами time_sec, bpm_value и uterus_value.
            Содержит объединенные и синхронизированные по времени данные о ЧСС и сокращениях матки.
    """
    united_df = pd.DataFrame(columns=['time_sec', 'bpm_value', 'uterus_value'])

    time_since_beginning: float = 0
    for bpm_f, uterus_f in zip(bpm_files, uterus_files):
        bpm_df: pd.DataFrame = pd.read_csv(bpm_f)
        uterus_df: pd.DataFrame = pd.read_csv(uterus_f)

        bpm_df['time_sec'] += time_since_beginning
        uterus_df['time_sec'] += time_since_beginning

        bpm_iter = bpm_df.itertuples(index=False)
        uterus_iter = uterus_df.itertuples(index=False)

        bpm_row = next(bpm_iter)
        uterus_row = next(uterus_iter)

        while (bpm_row is not None) and (uterus_row is not None):
            new_row: Dict[str, float] = get_new_row(bpm_row, uterus_row)
            united_df.loc[len(united_df)] = new_row

            if new_row['bpm_value'] != -1:
                bpm_row = next(bpm_iter, None)
            if new_row['uterus_value'] != -1:
                uterus_row = next(uterus_iter, None)

        time_since_beginning = united_df['time_sec'].max()

    return united_df

def get_new_row(bpm_row, uterus_row) -> Dict[str, float]:
    new_row: Dict[str, float] = {}

    bpm_time: Union[float, None] = None
    if bpm_row is not None:
        bpm_time = bpm_row.time_sec

    uterus_time: Union[float, None] = None
    if uterus_row is not None:
        uterus_time = uterus_row.time_sec

    EMPTY_VALUE: int = -1

    if (bpm_row is not None) and (uterus_row is not None):
        if bpm_time == uterus_time:
            new_row['time_sec'] = bpm_time
            new_row['bpm_value'] = bpm_row.value
            new_row['uterus_value'] = uterus_row.value
        else:
            new_row['time_sec'] = min(bpm_time, uterus_time)
            new_row['bpm_value'] = bpm_row.value if bpm_time < uterus_time else EMPTY_VALUE
            new_row['uterus_value'] = uterus_row.value if uterus_time < bpm_time else EMPTY_VALUE
    else:
        new_row['time_sec'] = bpm_time or uterus_time
        new_row['bpm_value'] = bpm_row.value if bpm_row is not None else EMPTY_VALUE
        new_row['uterus_value'] = uterus_row.value if uterus_row is not None else EMPTY_VALUE

    return new_row

from typing import List, Dict, Union

import pandas as pd


class Indicators:
    """
    Класс, содержащий методы для интерпритации данных ктг
    """
    def __init__(self, df: pd.DataFrame):
        self.__df: pd.DataFrame = df.copy()
        self.__basal_bpm_df: pd.DataFrame = self.__get_basal_bpm_df(bpm_df=df[['time_sec', 'bpm_value']].copy())
        self.__basal_bpm: float = self.__basal_bpm_df['bpm_value'].mean()

    @property
    def basal_bpm(self):
        """Базальная частота сердечных сокращений"""
        return self.__basal_bpm

    def __get_basal_bpm_df(self, bpm_df: pd.DataFrame) -> pd.DataFrame:
        basal_bpm = bpm_df['bpm_value'].mean()

        accelerations = self.get_accelerations(basal_bpm, bpm_df=bpm_df)
        decelerations = self.get_decelerations(basal_bpm, bpm_df=bpm_df)

        for a in accelerations:
            bpm_df.drop(index=range(a['start_index'], a['finish_index']), inplace=True)
        for d in decelerations:
            bpm_df.drop(index=range(d['start_index'], d['finish_index']), inplace=True)

        if len(accelerations) > 0 or len(decelerations) > 0:
            bpm_df = self.__get_basal_bpm_df(bpm_df=bpm_df)

        return bpm_df

    def get_accelerations(self, basal_bpm: float = None, bpm_df: pd.DataFrame = None) -> List[Dict[str, Union[int, float]]]:
        """
        Получение данных об акцелерациях.

        Params:
            basal_heart_rate: Базальная частота сердечных сокращений (уд./мин.).
            bpm (optional): Датафрейм, содержащий таймлайн с данными о ЧСС, в котором будет выполняться поиск акцелераций.
                Должен иметь столбцы time_sec и value.
                time_sec (float): Время с начала процедуры (сек.).
                value (float): ЧСС в момент измерения (уд./мин.).
                
                По умолчанию, поиск выполняется в датафрейме, переданном в конструктор класса.
        
        Returns:
            accelerations: Список словарей с данными о каждой акцелерации.
                Каждый словарь имеет поля:
                {
                    start_index (int): Индекс начала акцелерации в датафрейме bpm.
                    finish_index (int): Индекс окончания акцелерации в датафрейме bpm.
                    start_time (float): Время начала децеларации в секундах с начала процедуры.
                    finish_time (float): Время окончания децеларации в секундах с начала процедуры.
                }
        """

        if basal_bpm is None:
            basal_bpm = self.__basal_bpm
        if bpm_df is None:
            bpm_df = self.__df

        accelerations = []

        start_time = finish_time = 0
        start_index = finish_index = 0
        is_increase_start = is_increase_finish = False

        prev_time = 0
        for row in bpm_df.itertuples():
            current_time = row.time_sec

            if row.bpm_value - basal_bpm >= 15:
                if not is_increase_start:
                    start_time = row.time_sec
                    start_index = row.Index
                    is_increase_start = True
                elif current_time - prev_time > 5:
                    start_time = finish_time = 0
                    is_increase_start = is_increase_finish = False
                else:
                    finish_time = row.time_sec
                    finish_index = row.Index
            elif is_increase_start:
                is_increase_finish = True

            if is_increase_start and is_increase_finish:
                if finish_time - start_time >= 15:
                    accelerations.append({
                        'start_index': start_index,
                        'finish_index': finish_index,
                        'start_time': start_time,
                        'finish_time': finish_time
                    })

                start_time = finish_time = 0
                is_increase_start = is_increase_finish = False

            prev_time = current_time

        return accelerations

    def get_decelerations(self, basal_bpm: float = None, bpm_df: pd.DataFrame = None) -> List[Dict[str, Union[int, float]]]:
        """
        Получение данных об децелерациях.

        Params:
            basal_heart_rate: Базальная частота сердечных сокращений (уд./мин.).
            bpm (optional): Датафрейм, содержащий таймлайн с данными о ЧСС, в котором будет выполняться поиск децелераций.
                Должен иметь столбцы time_sec и value.
                time_sec (float): Время с начала процедуры (сек.).
                value (float): ЧСС в момент измерения (уд./мин.).

                По умолчанию, поиск выполняется в датафрейме, переданном в конструктор класса.

        Returns:
            decelerations: Список словарей с данными о каждой децелерации.
                Каждый словарь имеет поля:
                {
                    start_index (int): Индекс начала децелерации в датафрейме bpm.
                    finish_index (int): Индекс окончания децелерации в датафрейме bpm.
                    start_time (float): Время начала децеларации в секундах с начала процедуры.
                    finish_time (float): Время окончания децеларации в секундах с начала процедуры.
                }
        """

        if basal_bpm is None:
            basal_bpm = self.__basal_bpm
        if bpm_df is None:
            bpm_df = self.__df

        decelerations = []

        start_time = finish_time = 0
        start_index = finish_index = 0
        is_decrease_start = is_decrease_finish = False

        prev_time = 0
        for row in bpm_df.itertuples():
            current_time = row.time_sec

            if basal_bpm - row.bpm_value >= 15:
                if not is_decrease_start:
                    start_time = row.time_sec
                    start_index = row.Index
                    is_decrease_start = True
                elif current_time - prev_time > 5:
                    start_time = finish_time = 0
                    is_decrease_start = is_decrease_finish = False
                else:
                    finish_time = row.time_sec
                    finish_index = row.Index
            elif is_decrease_start:
                is_decrease_finish = True

            if is_decrease_start and is_decrease_finish:
                if finish_time - start_time >= 15:
                    decelerations.append({
                        'start_index': start_index,
                        'finish_index': finish_index,
                        'start_time': start_time,
                        'finish_time': finish_time
                    })

                start_time = finish_time = 0
                is_decrease_start = is_decrease_finish = False

            prev_time = current_time

        return decelerations

    def get_short_term_variability(self, bpm: pd.DataFrame = None) -> float:
        """Получение кратковременной вариабельности"""
        if bpm is None:
            bpm = self.__df

        stv: float = 0

        start_time = 0
        start_index = finish_index = 0

        prev_time = 0
        count = 0
        for row in bpm.itertuples():
            current_time = row.time_sec
            current_index = row.Index

            if start_time == 0:
                start_time = current_time
                start_index = current_index
            else:
                if current_time - prev_time > 2:
                    start_time = 0
                elif current_time - start_time > 3.75:
                    start_time = 0
                    finish_index = current_index

                    var_data = bpm.loc[start_index:finish_index]
                    max_bpm = var_data['bpm_value'].max()
                    min_bpm = var_data['bpm_value'].min()
                    amplitude = max_bpm - min_bpm

                    stv = (stv * count + amplitude) / (count + 1)
                    count += 1

            prev_time = current_time

        return stv

    def get_long_term_variability(self, bpm: pd.DataFrame = None) -> float:
        """Получение долговременной вариабельности"""
        if bpm is None:
            bpm = self.__df

        ltv: float = 0

        start_time = 0
        start_index = finish_index = 0

        prev_time = 0
        count = 0
        for row in bpm.itertuples():
            current_time = row.time_sec
            current_index = row.Index

            if start_time == 0:
                start_time = current_time
                start_index = current_index
            else:
                if current_time - prev_time > 15:
                    start_time = 0
                elif current_time - start_time > 3.75:
                    start_time = 0
                    finish_index = current_index

                    var_data = bpm.loc[start_index:finish_index]
                    max_bpm = var_data['bpm_value'].max()
                    min_bpm = var_data['bpm_value'].min()
                    amplitude = max_bpm - min_bpm

                    ltv = (ltv * count + amplitude) / (count + 1)
                    count += 1

            prev_time = current_time

        return ltv

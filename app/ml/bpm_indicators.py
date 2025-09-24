from typing import List, Dict, Union

import pandas as pd


class BpmIndicators:
    """
    Класс, содержащий методы для интерпритации данных о bpm
    """
    def __init__(self, bpm: pd.DataFrame):
        self.__bpm = bpm.copy()

    def get_basal_heart_rate(self, basal_bpm: pd.DataFrame = None) -> float:
        """
        Вычисление базальной частоты сердечных сокращений.

        Args:
            basal_bpm (optional): Датафрейм, содержащий таймлайн с данными о ЧСС.
                Должен иметь столбцы time_sec и value.
                time_sec (float): Время с начала процедуры в секундах.
                value (float): ЧСС в момент измерения.
        
        Returns:
            Базальная частота сердечных сокращений.
        """

        if basal_bpm is None:
            basal_bpm = self.__bpm.copy()

        basal_heart_rate = basal_bpm['value'].mean()

        accelerations = self.get_accelerations(basal_heart_rate, bpm=basal_bpm)
        decelerations = self.get_decelerations(basal_heart_rate, bpm=basal_bpm)

        for a in accelerations:
            basal_bpm.drop(index=range(a['start_index'], a['finish_index']), inplace=True)
        for d in decelerations:
            basal_bpm.drop(index=range(d['start_index'], d['finish_index']), inplace=True)

        if len(accelerations) > 0 or len(decelerations) > 0:
            basal_heart_rate = self.get_basal_heart_rate(basal_bpm=basal_bpm)

        return basal_heart_rate

    def get_accelerations(self, basal_heart_rate: float, bpm: pd.DataFrame = None) -> List[Dict[str, Union[int, float]]]:
        """
        Получение данных об акцелерациях.

        Params:
            basal_heart_rate: Базальная частота сердечных сокращений.
            bpm (optional): Датафрейм, содержащий таймлайн с данными о ЧСС, в котором будет выполняться поиск акцелераций.
                Должен иметь столбцы time_sec и value.
                time_sec (float): Время с начала процедуры в секундах.
                value (float): ЧСС в момент измерения.
                
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

        if bpm is None:
            bpm = self.__bpm.copy()

        accelerations = []

        start_time = finish_time = 0
        start_index = finish_index = 0
        is_increase_start = is_increase_finish = False

        prev_time = 0
        for row in bpm.itertuples():
            current_time = row.time_sec

            if row.value - basal_heart_rate >= 15:
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

    def get_decelerations(self, basal_heart_rate: float, bpm: pd.DataFrame = None) -> List[str, Union[int, float]]:
        """
        Получение данных об децелерациях.

        Params:
            basal_heart_rate: Базальная частота сердечных сокращений.
            bpm (optional): Датафрейм, содержащий таймлайн с данными о ЧСС, в котором будет выполняться поиск децелераций.
                Должен иметь столбцы time_sec и value.
                time_sec (float): Время с начала процедуры в секундах.
                value (float): ЧСС в момент измерения.

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

        if bpm is None:
            bpm = self.__bpm.copy()

        decelerations = []

        start_time = finish_time = 0
        start_index = finish_index = 0
        is_decrease_start = is_decrease_finish = False

        prev_time = 0
        for row in bpm.itertuples():
            current_time = row.time_sec

            if basal_heart_rate - row.value >= 15:
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
            bpm = self.__bpm

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
                    max_bpm = var_data['value'].max()
                    min_bpm = var_data['value'].min()
                    amplitude = max_bpm - min_bpm

                    stv = (stv * count + amplitude) / (count + 1)
                    count += 1

            prev_time = current_time

        return stv

    def get_long_term_variability(self, bpm: pd.DataFrame = None) -> float:
        """Получение долговременной вариабельности"""
        if bpm is None:
            bpm = self.__bpm

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
                    max_bpm = var_data['value'].max()
                    min_bpm = var_data['value'].min()
                    amplitude = max_bpm - min_bpm

                    ltv = (ltv * count + amplitude) / (count + 1)
                    count += 1

            prev_time = current_time

        return ltv

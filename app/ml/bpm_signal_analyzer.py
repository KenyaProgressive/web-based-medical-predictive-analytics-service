import pandas as pd
from typing import List, TypedDict, Dict, Union

class Deceleration(TypedDict):
    peak_time: float
    start_time: float
    end_time: float
    duration_sec: float
    amplitude: float
    peak_idx: int
    start_idx: int
    end_idx: int

class DecelerationsType(TypedDict):
    light: List[Deceleration]
    moderate: List[Deceleration]
    severe: List[Deceleration]
    prolongued: List[Deceleration]
    early: List[Deceleration]
    late: List[Deceleration]
    variable: List[Deceleration]

class Indicators:
    """
    Класс, содержащий методы для интерпритации данных ктг
    """
    def __init__(self, df: pd.DataFrame):
        self.__df: pd.DataFrame = df.copy()
        self.__basal_bpm_df: pd.DataFrame = self.__get_basal_bpm_df(bpm_df=self.__df.copy())

        self.__basal_bpm: float = self.__basal_bpm_df['bpm'].mean()

    @property
    def basal_bpm(self):
        """Базальная частота сердечных сокращений"""
        return self.__basal_bpm

    def __get_basal_bpm_df(self, bpm_df: pd.DataFrame) -> pd.DataFrame:
        basal_bpm = bpm_df['bpm'].mean()

        accelerations = self.get_accelerations(basal_bpm, bpm_df=bpm_df)
        decelerations = self.get_decelerations(basal_bpm, df=bpm_df)

        for a in accelerations:
            bpm_df.drop(index=range(a['start_index'], a['finish_index']), inplace=True)
        for d in decelerations:
            bpm_df.drop(index=range(d['start_idx'], d['end_idx']), inplace=True)

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
            current_time = row.time

            if row.bpm - basal_bpm >= 15:
                if not is_increase_start:
                    start_time = row.time
                    start_index = row.Index
                    is_increase_start = True
                elif current_time - prev_time > 5:
                    start_time = finish_time = 0
                    is_increase_start = is_increase_finish = False
                else:
                    finish_time = row.time
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

    def get_decelerations(
        self,
        basal_bpm: float = None,
        df: pd.DataFrame = None
    ) -> List[Deceleration]:
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
        if df is None:
            df = self.__df

        start_time = end_time = 0
        start_idx = end_idx = 0
        is_decrease_start = is_decrease_finish = False

        decelerations: List[Deceleration] = []

        prev_time = 0
        for row in df.itertuples():
            current_time = row.time

            if basal_bpm - row.bpm >= 15:
                if not is_decrease_start:
                    start_time = row.time
                    start_idx = row.Index
                    is_decrease_start = True
                elif current_time - prev_time > 5:
                    start_time = end_time = 0
                    is_decrease_start = is_decrease_finish = False
                else:
                    end_time = row.time
                    end_idx = row.Index
            elif is_decrease_start:
                is_decrease_finish = True

            if is_decrease_start and is_decrease_finish:
                if end_time - start_time >= 15:
                    curr_dec_df: pd.DataFrame = df.loc[start_idx:end_idx + 1]

                    peak_idx = curr_dec_df['bpm'].idxmin()
                    peak_time, peak_value = df.loc[peak_idx]['time'], df.loc[peak_idx]['bpm']

                    decelerations.append({
                        "peak_time": peak_time,
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration_sec": end_time - start_time,
                        "amplitude": basal_bpm - peak_value,
                        "peak_idx": peak_idx,
                        "start_idx": start_idx,
                        "end_idx": end_idx,
                    })

                start_time = end_time = 0
                is_decrease_start = is_decrease_finish = False

            prev_time = current_time

        return decelerations

    def get_decelerations_type(
        self,
        contractions: pd.DataFrame,
        decelerations: List[Deceleration]
    ) -> List[DecelerationsType]:
        decelerations_type: Dict[DecelerationsType] = {
            'light': [],
            'moderate': [],
            'severe': [],
            'prolongued': [],
            'early': [],
            'late': [],
            'variable': [],
        }

        for curr_decel in decelerations:
            if 180 <= curr_decel['duration_sec'] <= 600:
                decelerations_type['prolongued'].append(curr_decel)
            elif 15 <= curr_decel['amplitude'] <= 30:
                decelerations_type['light'].append(curr_decel)
            elif 16 <= curr_decel['amplitude'] <= 45:
                decelerations_type['moderate'].append(curr_decel)
            elif curr_decel['amplitude'] >= 45:
                decelerations_type['severe'].append(curr_decel)

            overlap = contractions[
                (contractions['end_time'] >= curr_decel['start_time'])
                & (contractions['start_time'] <= curr_decel['end_time'])
            ]
            for _, contraction in overlap.iterrows():
                if (
                    30 <= (curr_decel['start_time'] - contraction['start_time']) <= 60
                    and curr_decel['peak_time'] > contraction['peak_time']
                ):
                    decelerations_type['late'].append(curr_decel)
                elif (
                    abs(curr_decel['start_time'] - contraction['start_time']) <= 3
                    and abs(curr_decel['peak_time'] - contraction['peak_time']) <= 3
                    and abs(curr_decel['end_time'] - contraction['end_time']) <= 3
                ):
                    decelerations_type['early'].append(curr_decel)
                else:
                    decelerations_type['variable'].append(curr_decel)

        import pprint
        pprint.pprint(decelerations_type)

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
            current_time = row.time
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
                    max_bpm = var_data['bpm'].max()
                    min_bpm = var_data['bpm'].min()
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
            current_time = row.time
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
                    max_bpm = var_data['bpm'].max()
                    min_bpm = var_data['bpm'].min()
                    amplitude = max_bpm - min_bpm

                    ltv = (ltv * count + amplitude) / (count + 1)
                    count += 1

            prev_time = current_time

        return ltv

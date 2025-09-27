from typing import List, TypedDict, Dict
import pandas as pd

class HeartRateChange(TypedDict):
    start_time: float
    peak_time: float
    end_time: float
    duration_sec: float
    amplitude: float
    start_idx: int
    peak_idx: int
    end_idx: int

class DecelerationsType(TypedDict):
    light: List[HeartRateChange]
    moderate: List[HeartRateChange]
    severe: List[HeartRateChange]
    prolongued: List[HeartRateChange]
    early: List[HeartRateChange]
    late: List[HeartRateChange]
    variable: List[HeartRateChange]

class BpmSignalAnalyzer:
    """
    Класс, содержащий методы для интерпритации данных ктг
    """
    def __init__(self, df: pd.DataFrame):
        self.__df: pd.DataFrame = df.copy()
        self.__baseline: float = self.__get_baseline()

    @property
    def baseline(self):
        """Базальная частота сердечных сокращений"""
        return self.__baseline

    def __get_baseline(self, baseline_df: pd.DataFrame = None) -> float:
        if baseline_df is None:
            baseline_df = self.__df.copy()

        baseline: float = baseline_df['bpm'].mean()

        accelerations: List[HeartRateChange] = self.get_accelerations(baseline=baseline, df=baseline_df)
        decelerations: List[HeartRateChange] = self.get_decelerations(baseline=baseline, df=baseline_df)

        for a in accelerations:
            baseline_df.drop(index=range(a['start_idx'], a['end_idx']), inplace=True)
        for d in decelerations:
            baseline_df.drop(index=range(d['start_idx'], d['end_idx']), inplace=True)

        if len(accelerations) > 0 or len(decelerations) > 0:
            baseline = self.__get_baseline(baseline_df=baseline_df)

        return baseline

    def get_accelerations(
        self,
        baseline: float = None,
        df: pd.DataFrame = None
    ) -> List[HeartRateChange]:
        """
        Получение данных об акцелерациях.

        Params:
            baseline (optional): Базальная частота сердечных сокращений (уд./мин.).
            df (optional): Датафрейм, содержащий таймлайн с данными о ЧСС, в котором будет выполняться поиск акцелераций.
                Должен иметь столбцы time_sec и value.
                time (float): Время с начала процедуры (сек.).
                bpm (float): ЧСС в момент измерения (уд./мин.).
                
                По умолчанию, поиск выполняется в датафрейме, переданном в конструктор класса.
        
        Returns:
            List[HeartRateChange]: Список словарей с данными о каждой акцелерации.
                Каждый словарь имеет поля:
                {
                    start_time: (float): Время начала акцеларации (сек. с начала процедуры).
                    peak_time: (float): Время пика акцеларации (сек. с начала процедуры).
                    end_time: (float): Время окончания акцеларации (сек. с начала процедуры).
                    duration_sec: (float): Продолжительность акцелерации (сек.).
                    amplitude: (float): Амплитуда акцелерации (уд./мин.).
                    start_idx: (int): Индекс начала акцелерации.
                    peak_idx: (int): Индекс пика акцелерации.
                    end_idx: (int): Индекс окончания акцелерации.
                }
        """

        if baseline is None:
            baseline = self.__baseline
        if df is None:
            df = self.__df

        start_time = end_time = 0
        start_idx = end_idx = 0
        is_increase_start = is_increase_finish = False

        accelerations: List[HeartRateChange] = []

        prev_time = 0
        for row in df.itertuples():
            current_time = row.time

            if row.bpm - baseline >= 15:
                if not is_increase_start:
                    start_time = row.time
                    start_idx = row.Index
                    is_increase_start = True
                elif current_time - prev_time > 5:
                    start_time = end_time = 0
                    is_increase_start = is_increase_finish = False
                else:
                    end_time = row.time
                    end_idx = row.Index
            elif is_increase_start:
                is_increase_finish = True

            if is_increase_start and is_increase_finish:
                if end_time - start_time >= 15:
                    curr_act_df: pd.DataFrame = df.loc[start_idx:end_idx + 1]

                    peak_idx = curr_act_df['bpm'].idxmax()
                    peak_time, peak_value = df.loc[peak_idx]['time'], df.loc[peak_idx]['bpm']

                    accelerations.append({
                        "peak_time": float(peak_time),
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration_sec": end_time - start_time,
                        "amplitude": float(peak_value - baseline),
                        "peak_idx": peak_idx,
                        "start_idx": start_idx,
                        "end_idx": end_idx,
                    })

                start_time = end_time = 0
                is_increase_start = is_increase_finish = False

            prev_time = current_time

        return accelerations

    def get_decelerations(
        self,
        baseline: float = None,
        df: pd.DataFrame = None
    ) -> List[HeartRateChange]:
        """
        Получение данных об децелерациях.

        Params:
            baseline (optional): Базальная частота сердечных сокращений (уд./мин.).
            df (optional): Датафрейм, содержащий таймлайн с данными о ЧСС, в котором будет выполняться поиск децелераций.
                Должен иметь столбцы time_sec и value.
                time (float): Время с начала процедуры (сек.).
                bpm (float): ЧСС в момент измерения (уд./мин.).
                
                По умолчанию, поиск выполняется в датафрейме, переданном в конструктор класса.
        
        Returns:
            List[HeartRateChange]: Список словарей с данными о каждой децелерации.
                Каждый словарь имеет поля:
                {
                    start_time: (float): Время начала децеларации (сек. с начала процедуры).
                    peak_time: (float): Время пика децеларации (сек. с начала процедуры).
                    end_time: (float): Время окончания децеларации (сек. с начала процедуры).
                    duration_sec: (float): Продолжительность децелерации (сек.).
                    amplitude: (float): Амплитуда децелерации (уд./мин.).
                    start_idx: (int): Индекс начала децелерации.
                    peak_idx: (int): Индекс пика децелерации.
                    end_idx: (int): Индекс окончания децелерации.
                }
        """

        if baseline is None:
            baseline = self.__baseline
        if df is None:
            df = self.__df

        start_time = end_time = 0
        start_idx = end_idx = 0
        is_decrease_start = is_decrease_finish = False

        decelerations: List[HeartRateChange] = []

        prev_time = 0
        for row in df.itertuples():
            current_time = row.time

            if baseline - row.bpm >= 15:
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
                        "peak_time": float(peak_time),
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration_sec": end_time - start_time,
                        "amplitude": float(baseline - peak_value),
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
        decelerations: List[HeartRateChange] = None
    ) -> List[DecelerationsType]:
        if decelerations is None:
            decelerations = self.get_decelerations()

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

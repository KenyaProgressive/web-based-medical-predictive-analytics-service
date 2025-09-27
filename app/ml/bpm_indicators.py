import pandas as pd

class BpmIndicators:
    """
    Класс, содержащий методы для интерпритации данных о bpm
    """
    def __init__(self, bpm: pd.DataFrame):
        self.__bpm = bpm.copy()

    def get_basal_heart_rate(self, basal_bpm: pd.DataFrame = None):
        """
        Вычисление базальной ЧСС
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

    def get_accelerations(self, basal_heart_rate: float, bpm: pd.DataFrame = None):
        """
        Получение данных об акцелерациях
        """
        if bpm is None:
            bpm = self.__bpm.copy()

        accelerations = list()

        start_time = finish_time = 0
        start_index = finish_index = 0
        is_increase_start = is_increase_finish = False

        for row in bpm.itertuples():
            if row.value - basal_heart_rate >= 15:
                if not is_increase_start:
                    start_time = row.time_sec
                    start_index = row.Index
                    is_increase_start = True
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

        return accelerations

    def get_decelerations(self, basal_heart_rate: float, bpm: pd.DataFrame = None):
        """
        Получение данных о децелерациях
        """
        if bpm is None:
            bpm = self.__bpm.copy()

        decelerations = list()

        start_time = finish_time = 0
        start_index = finish_index = 0
        is_decrease_start = is_decrease_finish = False

        for row in bpm.itertuples():
            if basal_heart_rate - row.value >= 15:
                if not is_decrease_start:
                    start_time = row.time_sec
                    start_index = row.Index
                    is_decrease_start = True
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

        return decelerations

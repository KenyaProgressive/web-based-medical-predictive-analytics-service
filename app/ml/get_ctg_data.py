import pandas as pd
from typing import TypedDict, List

from app.const import MIN_TIME, MAX_TIME
from app.ml.uterus_signal_analyzer import find_contractions
from app.ml.bpm_signal_analyzer import HeartRateChange, BpmSignalAnalyzer

class CtgData(TypedDict):
    baseline_bpm: float
    short_term_variability: float
    long_term_variability: float
    accelerations_per_30_min: List[HeartRateChange]
    decelerations_per_30_min: List[HeartRateChange]

def get_ctg_data(bpm_df: pd.DataFrame, uterus_df: pd.DataFrame) -> CtgData:
    # print(bpm_df['time'].max())
    time = bpm_df['time'].max() - bpm_df['time'].min()

    contractions = find_contractions(uterus_df)[0]

    ctg_data: CtgData = {}
    bpm_anal = BpmSignalAnalyzer(bpm_df)

    baseline_bpm = bpm_anal.get_baseline()
    ctg_data['baseline'] = baseline_bpm
    ctg_data['short_term_variability'] = bpm_anal.get_short_term_variability()
    ctg_data['long_term_variability'] = bpm_anal.get_long_term_variability()

    if MIN_TIME <= time <= MAX_TIME:
        ctg_data['accelerations_per_30_min'] = bpm_anal.get_accelerations(baseline_bpm)
    elif time < MIN_TIME:
        ctg_data['accelerations_per_30_min'] = []
    elif time > MAX_TIME:
        raise ValueError(
            'The data was transmitted in too long a period of time. Expected 30 minutes'
        )

    if MIN_TIME <= time <= MAX_TIME:
        decelerations = bpm_anal.get_decelerations(baseline_bpm)
        ctg_data['decelerations_per_30_min'] = bpm_anal.get_decelerations_type(contractions, decelerations)
    elif time < MIN_TIME:
        ctg_data['decelerations_per_30_min'] = []
    elif time > MAX_TIME:
        raise ValueError(
            'The data was transmitted in too long a period of time. Expected 30 minutes'
        )

    return ctg_data

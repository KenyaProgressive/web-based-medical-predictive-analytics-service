from typing import Tuple
import pandas as pd

from app.ml.uterus_signal_analyzer import find_contractions
from app.ml.bpm_signal_analyzer import BpmSignalAnalyzer

def get_ctg_data() -> Tuple:
    bpm_df = pd.read_csv('bpm.csv')
    uterus_df = pd.read_csv('uterus.csv')

    MIN_TIME = 60 * 28
    MAX_TIME = 60 * 32
    time = bpm_df['time'].max() - bpm_df['time'].min()

    contractions = find_contractions(uterus_df)

    ctg_data = {}
    bpm_anal = BpmSignalAnalyzer(bpm_df)

    ctg_data['baseline'] = bpm_anal.baseline
    ctg_data['short_term_variability'] = bpm_anal.get_short_term_variability()
    ctg_data['long_term_variability'] = bpm_anal.get_long_term_variability()

    if MIN_TIME <= time <= MAX_TIME:
        ctg_data['accelerations_per_30_min'] = bpm_anal.get_accelerations()
    elif time < MIN_TIME:
        ctg_data['accelerations_per_30_min'] = ['not enough data to calculate']

    if MIN_TIME <= time <= MAX_TIME:
        decelerations = bpm_anal.get_decelerations()
        ctg_data['decelerations_per_30_min'] = bpm_anal.get_decelerations()
        ctg_data['decelerations_type'] = bpm_anal.get_decelerations_type(contractions, decelerations)
    elif time < MIN_TIME:
        ctg_data['decelerations_per_30_min'] = ['not enough data to calculate']
        ctg_data['decelerations_type'] = ['not enough data to calculate']

    return ctg_data

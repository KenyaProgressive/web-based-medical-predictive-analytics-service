import pandas as pd
from glob import glob

from app.ml.data_conversion import join_data
from app.ml.indicators import Indicators


bpm_csv = sorted(glob('db/data/hypoxia/4/bpm/*.csv'))
uterus_csv = sorted(glob('db/data/hypoxia/4/uterus/*.csv'))

# print(1)
test_data = join_data(bpm_csv, uterus_csv)
# print(2)
test_data.to_csv('test.csv', index=False, float_format="%.6f")

# test_data = pd.read_csv('test.csv')

indicators = Indicators(test_data)

basal = indicators.basal_bpm
print(basal)
print(indicators.get_accelerations())
print(indicators.get_decelerations())
print(indicators.get_short_term_variability())
print(indicators.get_long_term_variability())
print(test_data['time_sec'].max())

# for i in range(1, 26):
#     test_csv = sorted(glob(f'db/data/hypoxia/{i}/bpm/*.csv'))

#     test_data = join_data(test_csv)
#     # test_data.to_csv('test.csv', index=True, float_format="%.6f")

#     bpm_indicators = BpmIndicators(test_data)

#     try:
#         basal = bpm_indicators.get_basal_heart_rate()
#         bpm_indicators.get_accelerations(basal_heart_rate=basal)
#         bpm_indicators.get_decelerations(basal_heart_rate=basal)
#         bpm_indicators.get_short_term_variability()
#         bpm_indicators.get_long_term_variability()
#     except:
#         print(f'{i} ошибся!')
#     else:
#         print(f'{i} проверено!')

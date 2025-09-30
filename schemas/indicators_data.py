from pydantic import BaseModel
from typing import List
from pandas._typing import Scalar

class IndicatorsData(BaseModel):
    accelerations: List[Scalar]
    decelarations: List[Scalar]
    basal_heart_rate: float





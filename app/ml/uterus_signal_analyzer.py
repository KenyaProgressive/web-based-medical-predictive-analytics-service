
import pandas as pd
import numpy as np
from scipy.signal import medfilt, find_peaks
from typing import Tuple, List, Optional, TypedDict

class Contraction(TypedDict):
    peak_time: float
    start_time: float
    end_time: float
    duration_sec: float
    amplitude: float
    peak_idx: int
    interval_to_next_sec: Optional[float]

class FrequencyWindow(TypedDict):
    window_start: float
    window_end: float
    contractions_count: int

def find_contractions(
    df: pd.DataFrame,
    fs: int = 4,
    window_minutes: int = 10,
    baseline_percentile: int = 20,
    min_amplitude: float = 10,
    min_duration_sec: float = 20,
    merge_gap_sec: float = 3,
    prominence: float = 5,
    width: int = 30,
) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
    """
    Поиск схваток по сигналам сокращения матки

    Args:
        df: DataFrame с колонками ["time", "uterus"].
        fs: Частота дискретизации (Гц).
        window_minutes: Окно анализа для подсчета частоты схваток (минуты).
        baseline_percentile: Процентиль для определения базального тонуса.
        min_amplitude: Минимальная амплитуда схватки.
        min_duration_sec: Минимальная длительность схватки (секунды).
        merge_gap_sec: Максимальный интервал между схватками для объединения (секунды).
        prominence: Минимальная высота пика для поиска.
        width: Минимальная ширина пика для поиска.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, float]:
            - contractions_df: DataFrame с информацией о найденных схватках.
            - freq_df: DataFrame с частотой схваток в каждом временном окне.
            - baseline: Значение базального тонуса.
    """
    uterus: np.ndarray = df["uterus"].values
    time: np.ndarray = df["time"].values

    uterus_med: np.ndarray = medfilt(uterus, kernel_size=5)
    baseline: float = np.percentile(uterus_med, baseline_percentile)

    peaks, _ = find_peaks(
        uterus_med,
        prominence=prominence,
        width=width,
        distance=fs * 2,
    )

    contractions: List[Contraction] = []

    for peak in peaks:
        amplitude: float = uterus_med[peak] - baseline
        if amplitude < min_amplitude:
            continue

        start: int = peak
        while start > 0 and uterus_med[start] > baseline + 0.5 * amplitude:
            start -= 1

        end: int = peak
        while end < len(uterus_med) - 1 and uterus_med[end] > baseline + 0.5 * amplitude:
            end += 1

        duration: float = (end - start) / fs
        if duration < min_duration_sec:
            continue

        contractions.append(
            {
                "peak_time": float(time[peak]),
                "start_time": float(time[start]),
                "end_time": float(time[end]),
                "duration_sec": float(duration),
                "amplitude": float(amplitude),
                "peak_idx": int(peak),
                "interval_to_next_sec": None,
            }
        )

    if contractions:
        merged_contractions: List[Contraction] = [contractions[0]]
        for i in range(1, len(contractions)):
            prev: Contraction = merged_contractions[-1]
            curr: Contraction = contractions[i]
            gap: float = curr["start_time"] - prev["end_time"]
            if gap <= merge_gap_sec:
                prev["end_time"] = curr["end_time"]
                prev["duration_sec"] = prev["end_time"] - prev["start_time"]
                prev["amplitude"] = max(prev["amplitude"], curr["amplitude"])
            else:
                merged_contractions.append(curr)
        contractions = merged_contractions

    for j in range(len(contractions) - 1):
        contractions[j]["interval_to_next_sec"] = (
            contractions[j + 1]["peak_time"] - contractions[j]["peak_time"]
        )

    if contractions:
        contractions[-1]["interval_to_next_sec"] = None

    contractions_df: pd.DataFrame = pd.DataFrame(contractions)

    # freq_results: List[FrequencyWindow] = []
    # window_sec: int = window_minutes * 60

    # for start in np.arange(0, time[-1], window_sec):
    #     end: float = start + window_sec
    #     count: int = np.sum(
    #         (contractions_df["peak_time"] >= start) &
    #         (contractions_df["peak_time"] < end)
    #     )
    #     freq_results.append(
    #         {
    #             "window_start": start,
    #             "window_end": end,
    #             "contractions_count": int(count),
    #         }
    #     )

    # freq_df: pd.DataFrame = pd.DataFrame(freq_results)

    # return contractions_df, freq_df, baseline
    return contractions_df, baseline

def calculate_contraction_intensity(contractions: List[Contraction]) -> float:
    """
    Рассчитывает среднюю амплетуду схваток
    """
    if not contractions:
        return 0.0
    amplitudes = [c["amplitude"] for c in contractions]
    return sum(amplitudes) / len(amplitudes)

def calculate_contraction_regularity(contractions: List[Contraction]) -> Tuple[float, float]:
    """
    Рассчитывает средний интервал между схватками и его стандартное отклонение
    """
    intervals = [c["interval_to_next_sec"] for c in contractions if c["interval_to_next_sec"] is not None]
    if not intervals:
        return 0.0, 0.0
    mean_interval = sum(intervals) / len(intervals)
    std_interval = (sum((x - mean_interval) ** 2 for x in intervals) / len(intervals)) ** 0.5
    return mean_interval, std_interval

def calculate_frequency_dynamics(
    contractions: List[Contraction],
    window_minutes: int = 10
) -> List[FrequencyWindow]:
    """
    Рассчитывает динамику частоты схваток в каждом временном окне
    """
    if not contractions:
        return []
    window_sec = window_minutes * 60
    start_time = contractions[0]["start_time"]
    end_time = contractions[-1]["end_time"]
    freq_results: List[FrequencyWindow] = []
    for window_start in np.arange(start_time, end_time, window_sec):
        window_end = window_start + window_sec
        count = sum(
            1 for c in contractions
            if window_start <= c["peak_time"] < window_end
        )
        freq_results.append({
            "window_start": window_start,
            "window_end": window_end,
            "contractions_count": count,
        })
    return freq_results

def calculate_duration_statistics(contractions: List[Contraction]) -> Tuple[float, float, float]:
    """
    Рассчитывает среднюю, минимальную и максимальную длительность схваток
    """
    if not contractions:
        return 0.0, 0.0, 0.0
    durations = [c["duration_sec"] for c in contractions]
    mean_duration = sum(durations) / len(durations)
    min_duration = min(durations)
    max_duration = max(durations)
    return mean_duration, min_duration, max_duration
import pandas as pd
import numpy as np
from typing import Optional


MIN_LOW_PHASE_DAYS = 6
MIN_HIGH_PHASE_DAYS = 3
COVERLINE_OFFSET   = 0.1  # °C above highest of the 6 low-phase temps


def detect_ovulation(
    cycle_df: pd.DataFrame,
    temp_col: str = "temperature_deviation",
    day_col:  str = "cycle_day",
) -> dict:
    """
    Detect ovulation in a single cycle using the FAM thermal shift rule.

    Rules:
    - Requires at least 6 non-null temperatures before detection can begin
    - Coverline = highest of the previous 6 temps + 0.1°C
    - Ovulation confirmed when 3 consecutive temps all exceed the coverline
    - Ovulation day = day before the first of the 3 elevated readings

    Parameters
    ----------
    cycle_df : pd.DataFrame
        DataFrame for a single cycle, sorted by cycle day.
    temp_col : str
        Column name for temperature deviation.
    day_col : str
        Column name for cycle day.

    Returns
    -------
    dict with keys:
        ovulation_day       : int or None
        coverline           : float or None
        follicular_days     : list[int] or None
        luteal_days         : list[int] or None
        status              : str  ("detected", "insufficient_data", "not_detected")
    """
    null_result = {
        "ovulation_day":   None,
        "coverline":       None,
        "follicular_days": None,
        "luteal_days":     None,
    }

    df = cycle_df[[day_col, temp_col]].dropna().reset_index(drop=True)

    # Not enough data to attempt detection
    if len(df) < MIN_LOW_PHASE_DAYS + MIN_HIGH_PHASE_DAYS:
        return {**null_result, "status": "insufficient_data"}

    days  = df[day_col].tolist()
    temps = df[temp_col].tolist()

    # Slide through each possible ovulation window
    for i in range(MIN_LOW_PHASE_DAYS, len(temps) - MIN_HIGH_PHASE_DAYS + 1):
        low_phase   = temps[i - MIN_LOW_PHASE_DAYS : i]
        coverline   = max(low_phase) + COVERLINE_OFFSET
        high_phase  = temps[i : i + MIN_HIGH_PHASE_DAYS]

        if all(t > coverline for t in high_phase):
            ovulation_day   = days[i - 1]  # day before first elevated reading
            follicular_days = [d for d in cycle_df[day_col] if d <= ovulation_day]
            luteal_days     = [d for d in cycle_df[day_col] if d >  ovulation_day]

            return {
                "ovulation_day":   ovulation_day,
                "coverline":       round(coverline, 3),
                "follicular_days": follicular_days,
                "luteal_days":     luteal_days,
                "status":          "detected",
            }

    return {**null_result, "status": "not_detected"}


def label_cycle_phases(
    cycle_df: pd.DataFrame,
    temp_col: str = "temperature_deviation",
    day_col:  str = "cycle_day",
) -> pd.DataFrame:
    """
    Add phase labels and coverline to a cycle DataFrame.

    Returns the same DataFrame with two new columns:
        phase       : "follicular", "luteal", or "unknown"
        coverline   : float or NaN
    """
    result = detect_ovulation(cycle_df, temp_col=temp_col, day_col=day_col)
    df     = cycle_df.copy()

    if result["status"] == "detected":
        df["phase"] = df[day_col].apply(
            lambda d: "follicular" if d <= result["ovulation_day"] else "luteal"
        )
        df["coverline"] = result["coverline"]
    else:
        df["phase"]     = "unknown"
        df["coverline"] = np.nan

    return df, result
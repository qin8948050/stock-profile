from typing import List
import pandas as pd
import numpy as np
from .multi_metric import MultiMetric

class PEGRatioMetric(MultiMetric):
    """
    Configuration for the PEG Ratio metric chart.
    PEG Ratio = PE Ratio / Net Income Growth Rate
    """
    metric_name = "peg_ratio"
    chart_title = "PEG比率"
    dependent_metrics = ["pe_ratio", "net_income"]

    def _calculate_series_values(self, aligned_df: pd.DataFrame) -> pd.Series:
        # Calculate Net Income Growth Rate
        ni_growth = aligned_df["net_income"].pct_change() * 100
        
        # Calculate PEG
        peg = aligned_df["pe_ratio"] / ni_growth.replace(0, np.nan)
        
        return peg.dropna()

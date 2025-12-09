from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from schemas.chart import ChartData

# --- Unit Constants ---
# Using descriptive names for divisors to avoid magic numbers.
UNIT_ONE = 1
UNIT_THOUSAND = 1_000
UNIT_TEN_THOUSAND = 10_000
UNIT_MILLION = 1_000_000
UNIT_HUNDRED_MILLION = 100_000_000  # For "亿"
UNIT_BILLION = 1_000_000_000

# A mapping for convenience, though direct use of constants is clearer.
UNITS = {
    "one": UNIT_ONE,
    "thousand": UNIT_THOUSAND,
    "ten_thousand": UNIT_TEN_THOUSAND,
    "million": UNIT_MILLION,
    "hundred_million": UNIT_HUNDRED_MILLION,
    "billion": UNIT_BILLION,
}

# (ratio_label, value_label, etc. remain the same)
ratio_label={
    "show": True,
    "position": "top",
    "formatter": "{c}%",
    "color": "#ffffff",
    "fontSize": 14,
    "fontWeight": "bold",
    "textBorderColor": "rgba(0,0,0,0.8)",
    "textBorderWidth": 3,
    "textShadowColor": "rgba(0,0,0,0.4)",
    "textShadowBlur": 4,
}
value_label={"show": True, "position": "inside", "fontSize": 14, "formatter": "{c}"}


class BaseMetric(ABC):
    """
    Abstract base class for defining a financial metric's chart configuration.
    Subclasses should provide metric-specific configurations.
    """
    metric_name: str = "base_metric"
    # A list of metric names that this metric depends on.
    # For single-metric charts, this will be an empty list.
    dependencies: List[str] = []
    # Subclasses should override this with a descriptive unit constant, e.g., UNIT_HUNDRED_MILLION
    value_unit: int = UNIT_ONE

    @abstractmethod
    def get_chart_data(self, time_series_data: Dict[str, List[Dict[str, Any]]]) -> ChartData:
        """
        Generates the ChartData object for the metric using the provided time series data.
        For single-metric charts, the dictionary will contain one entry.
        For calculated metrics, it will contain entries for each dependency.
        """
        raise NotImplementedError

    def _process_time_series_data(
        self,
        time_series_data: List[Dict[str, Any]],
        metric_name: Optional[str] = None
    ) -> (List[str], List[float]):
        """
        Processes raw time series data using pandas for value extraction and conversion.
        Returns categories (years) and processed values.
        If metric_name is provided, it's used for error messaging.
        """
        if not time_series_data:
            return [], []

        df = pd.DataFrame(time_series_data)

        if 'value' not in df.columns:
            df['value'] = 0
        df['value'] = df['value'].fillna(0)

        categories = df["year"].tolist()
        
        # Use the class attribute for division based on the defined unit constant
        divisor = self.value_unit
        if divisor == 0: # Avoid division by zero
            divisor = 1
            
        values = (df["value"] / divisor).round(2).tolist()
        
        return categories, values

    def _calculate_growth_rates(self, values: List[float]) -> List[float]:
        """
        Calculates year-over-year growth rates using pandas.
        """
        if not values:
            return []
        s = pd.Series(values)
        growth = s.pct_change() * 100
        # Replace inf/-inf with 0 (for divisions by zero) and fill initial NaN with 0
        growth_rates = growth.replace([np.inf, -np.inf], 0).fillna(0)
        return growth_rates.round(2).tolist()

from .base_metric import UNIT_HUNDRED_MILLION
from .single_metric import SingleMetric

class CashAtEndOfPeriodMetric(SingleMetric):
    """
    Configuration for the Cash at End of Period metric chart.
    Inherits the common data processing and chart generation logic from SingleMetric.
    """
    metric_name = "cash_at_end_of_period"
    chart_title = "期末现金流净额（亿/美元）"
    series_name = "净额"
    
    # This specific metric uses "hundred million" as its unit.
    value_unit = UNIT_HUNDRED_MILLION

from .base_metric import UNIT_HUNDRED_MILLION
from .single_metric import SingleMetric

class TotalLiabilitiesMetric(SingleMetric):
    """
    Configuration for the Total Liabilities metric chart.
    Inherits the common data processing and chart generation logic from SingleMetric.
    """
    metric_name = "total_liabilities"
    chart_title = "总负债（亿/美元）"
    series_name = "负债"
    
    # This specific metric uses "hundred million" as its unit.
    value_unit = UNIT_HUNDRED_MILLION

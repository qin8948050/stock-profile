from .base_metric import UNIT_HUNDRED_MILLION
from .single_metric import SingleMetric

class TotalAssetsMetric(SingleMetric):
    """
    Configuration for the Total Assets metric chart.
    Inherits the common data processing and chart generation logic from SingleMetric.
    """
    metric_name = "total_assets"
    chart_title = "总资产（亿/美元）"
    series_name = "资产"
    
    # This specific metric uses "hundred million" as its unit.
    value_unit = UNIT_HUNDRED_MILLION

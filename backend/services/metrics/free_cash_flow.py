from .base_metric import UNIT_HUNDRED_MILLION
from .single_metric import SingleMetric


class FreeCashFlowMetric(SingleMetric):
    """
    Configuration for the Free Cash Flow metric chart.
    Inherits the common data processing and chart generation logic from SingleMetric.
    """
    metric_name = "free_cash_flow"
    chart_title = "自由现金流（亿/美元）"
    series_name = "净额"

    # This specific metric uses "hundred million" as its unit.
    value_unit = UNIT_HUNDRED_MILLION

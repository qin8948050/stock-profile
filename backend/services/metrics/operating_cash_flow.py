from .base_metric import UNIT_HUNDRED_MILLION
from .single_metric import SingleMetric


class OperatingCashFlowMetric(SingleMetric):
    """
    Configuration for the Operating Cash Flow metric chart.
    Inherits the common data processing and chart generation logic from SingleMetric.
    """
    metric_name = "operating_cash_flow"
    chart_title = "经营现金流（亿/美元）"
    series_name = "净额"

    # This specific metric uses "hundred million" as its unit.
    value_unit = UNIT_HUNDRED_MILLION

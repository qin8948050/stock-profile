from .ratio_metric import RatioMetric


class FreeCashFlowToNetIncomeRatioMetric(RatioMetric):
    """
    Calculates the ratio of free cash flow to net income.
    This metric indicates how much of that earning is converted into cash that is available for shareholders after funding operations and capital expenditures.
    """
    metric_name = "free_cash_flow_to_net_income_ratio"
    chart_title = "自由现金流与净利润比率"
    numerator_metric = "free_cash_flow"
    denominator_metric = "net_income"

from .ratio_metric import RatioMetric


class OperatingCashFlowToNetIncomeRatioMetric(RatioMetric):
    """
    Calculates the ratio of operating cash flow to net income.
    This metric indicates whether a company's reported earnings are backed by actual cash from its operations.
    """
    metric_name = "operating_cash_flow_to_net_income_ratio"
    chart_title = "经营现金流与净利润比率"
    numerator_metric = "operating_cash_flow"
    denominator_metric = "net_income"

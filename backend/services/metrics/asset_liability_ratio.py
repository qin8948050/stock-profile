from .ratio_metric import RatioMetric

class AssetLiabilityRatioMetric(RatioMetric):
    """
    Configuration for the Asset-Liability Ratio metric chart.
    This metric is calculated as: Total Assets / Total Liabilities.
    It inherits the common calculation and chart generation logic from RatioMetric.
    """
    metric_name = "asset_liability_ratio"
    chart_title = "资产负债率"

    @property
    def numerator_metric(self) -> str:
        return "total_assets"

    @property
    def denominator_metric(self) -> str:
        return "total_liabilities"

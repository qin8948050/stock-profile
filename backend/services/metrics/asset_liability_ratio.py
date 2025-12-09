from typing import List, Dict, Any
import pandas as pd
from .base_metric import BaseMetric, ratio_label, value_label
from schemas.chart import ChartData, ChartAxis, ChartSeries, ChartTitle, ChartLegend

class AssetLiabilityRatioMetric(BaseMetric):
    """
    Configuration for the Asset-Liability Ratio metric chart.
    This metric is calculated as: Total Assets / Total Liabilities.
    """
    metric_name = "asset_liability_ratio"
    # This metric depends on two other metrics.
    dependencies = ["total_assets", "total_liabilities"]

    def get_chart_data(self, time_series_data: Dict[str, List[Dict[str, Any]]]) -> ChartData:
        """
        Calculates the asset-liability ratio from the provided time series data.
        """
        total_assets_data = time_series_data.get("total_assets")
        total_liabilities_data = time_series_data.get("total_liabilities")

        if not total_assets_data or not total_liabilities_data:
            return ChartData(
                title=ChartTitle(text="Asset-Liability Ratio (No Data)"),
                series=[]
            )

        # --- Data Processing ---
        df_assets = pd.DataFrame(total_assets_data).set_index("year")
        df_liabilities = pd.DataFrame(total_liabilities_data).set_index("year")

        # Align data by year and calculate the ratio
        df_ratio = (df_assets["value"] / df_liabilities["value"]).dropna()
        
        categories = df_ratio.index.tolist()
        values = df_ratio.round(2).tolist()
        growth_rates = self._calculate_growth_rates(values)
        return ChartData(
            title=ChartTitle(text="资产负债率"),
            legend=ChartLegend(data=["比率","增长率"], right='right'),
            xAxis=[ChartAxis(type="category", data=categories, name="年份", nameLocation="middle", nameGap=30, axisLabel={"show": True})],
            yAxis=[
                ChartAxis(type="value", axisLabel={"formatter": "{value}"}),
                ChartAxis(type="value", position="right", axisLabel={"formatter": "{value} %"})
            ],
            series=[
                ChartSeries(name="比率", type="bar", data=values, label=value_label),
                ChartSeries(name="增长率", type="line", yAxisIndex=1, data=growth_rates, smooth=True,
                            label=ratio_label),
            ]
        )

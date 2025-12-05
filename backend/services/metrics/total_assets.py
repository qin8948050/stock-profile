from typing import List, Dict, Any
# Import the new unit constants from the base metric module
from .base_metric import BaseMetric, ratio_label, value_label, UNIT_HUNDRED_MILLION
from schemas.chart import ChartData, ChartAxis, ChartSeries, ChartTitle, ChartLegend

class TotalAssetsMetric(BaseMetric):
    """
    Configuration for the Total Assets metric chart.
    Inherits data processing logic from BaseMetric and specifies its own configurations.
    """
    metric_name = "total_assets"
    # Use the descriptive constant for the unit, making the code self-documenting.
    value_unit = UNIT_HUNDRED_MILLION

    def get_chart_data(self, time_series_data: List[Dict[str, Any]]) -> ChartData:
        """
        Generates the chart data by leveraging the common processing methods from the base class.
        """
        if not time_series_data:
            return ChartData(
                title=ChartTitle(text="Total Assets (No Data)"),
                series=[]
            )

        # Use the inherited helper methods for data processing
        categories, values = self._process_time_series_data(time_series_data)
        growth_rates = self._calculate_growth_rates(values)

        return ChartData(
            title=ChartTitle(text="总资产（亿/美元）"),
            legend=ChartLegend(data=["资产", "增长率"], right='right'),
            xAxis=[ChartAxis(type="category", data=categories, name="年份", nameLocation="middle", nameGap=30, axisLabel={"show": True})],
            yAxis=[
                ChartAxis(type="value", axisLabel={"formatter": "{value}"}),
                ChartAxis(type="value", position="right", axisLabel={"formatter": "{value} %"})
            ],
            series=[
                ChartSeries(name="资产", type="bar", data=values, label=value_label),
                ChartSeries(name="增长率", type="line", yAxisIndex=1, data=growth_rates, smooth=True, label=ratio_label),
            ]
        )

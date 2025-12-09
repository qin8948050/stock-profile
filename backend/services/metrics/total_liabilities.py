from typing import List, Dict, Any
from .base_metric import BaseMetric, value_label, ratio_label, UNIT_HUNDRED_MILLION
from schemas.chart import ChartData, ChartAxis, ChartSeries, ChartTitle, ChartLegend

class TotalLiabilitiesMetric(BaseMetric):
    """
    Configuration for the Total Assets metric chart.
    """
    metric_name = "total_liabilities"
    value_unit = UNIT_HUNDRED_MILLION

    def get_chart_data(self, time_series_data: Dict[str, List[Dict[str, Any]]]) -> ChartData:
        """
        Generates the chart data by leveraging the common processing methods from the base class.
        """
        # For a single metric, the data is under its own metric_name key.
        total_liabilities_data = time_series_data.get(self.metric_name, [])

        if not total_liabilities_data:
            return ChartData(
                title=ChartTitle(text="Total Liabilities (No Data)"),
                series=[]
            )

        categories, values = self._process_time_series_data(total_liabilities_data)
        growth_rates = self._calculate_growth_rates(values)

        return ChartData(
            title=ChartTitle(text="总负债（亿/美元）"),
            legend=ChartLegend(data=["负债", "增长率"],right='right'),
            xAxis=[ChartAxis(type="category", data=categories, name="年份", nameLocation="middle", nameGap=30,axisLabel={"show": True})],
            yAxis=[
                ChartAxis(type="value",axisLabel={"formatter": "{value}"}), # Updated Y-axis label
                ChartAxis(type="value",position="right", axisLabel={"formatter": "{value} %"})
            ],
            series=[
                ChartSeries(name="负债", type="bar", data=values,label=value_label),
                ChartSeries(name="增长率", type="line", yAxisIndex=1, data=growth_rates, smooth=True,label=ratio_label),
            ]
        )

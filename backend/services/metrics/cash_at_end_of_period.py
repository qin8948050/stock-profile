from typing import List, Dict, Any
from .base_metric import BaseMetric, ratio_label, value_label, UNIT_HUNDRED_MILLION
from schemas.chart import ChartData, ChartAxis, ChartSeries, ChartTitle, ChartLegend

class CashAtEndOfPeriodMetric(BaseMetric):
    """
    Configuration for the Total Assets metric chart.
    """
    metric_name = "cash_at_end_of_period"
    value_unit = UNIT_HUNDRED_MILLION

    def get_chart_data(self, time_series_data: List[Dict[str, Any]]) -> ChartData:
        if not time_series_data:
            return ChartData(
                title=ChartTitle(text="Total Assets (No Data)"),
                series=[]
            )

        categories, values = self._process_time_series_data(time_series_data)
        growth_rates = self._calculate_growth_rates(values)

        return ChartData(
            title=ChartTitle(text="期末现金流净额（亿/美元）"),
            legend=ChartLegend(data=["净额", "增长率"],right='right'),
            xAxis=[ChartAxis(type="category", data=categories, name="年份", nameLocation="middle", nameGap=30,axisLabel={"show": True})],
            yAxis=[
                ChartAxis(type="value",axisLabel={"formatter": "{value}"}), # Updated Y-axis label
                ChartAxis(type="value",position="right", axisLabel={"formatter": "{value} %"})
            ],
            series=[
                ChartSeries(name="净额", type="bar", data=values,label=value_label),
                ChartSeries(name="增长率", type="line", yAxisIndex=1, data=growth_rates, smooth=True,label=ratio_label),
            ]
        )

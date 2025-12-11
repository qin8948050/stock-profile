from abc import abstractmethod
from typing import List, Dict, Any
from .base_metric import BaseMetric, ratio_label, value_label
from schemas.chart import ChartData, ChartAxis, ChartSeries, ChartTitle, ChartLegend

class SingleMetric(BaseMetric):
    """
    Abstract base class for metrics that correspond to a single time series.
    It handles the common logic of fetching its own data, processing it,
    calculating growth rates, and generating a standard chart.

    Subclasses must define `metric_name`, `chart_title`, `series_name`,
    and can override `value_unit`.
    """
    @property
    @abstractmethod
    def chart_title(self) -> str:
        """The title for the chart."""
        raise NotImplementedError

    @property
    @abstractmethod
    def series_name(self) -> str:
        """The name for the primary data series in the chart (e.g., "资产", "收入")."""
        raise NotImplementedError

    def get_chart_data(self, time_series_data: Dict[str, List[Dict[str, Any]]]) -> ChartData:
        """
        Generates the chart data by processing the time series data for this metric.
        """
        metric_data = time_series_data.get(self.metric_name, [])

        if not metric_data:
            return ChartData(
                title=ChartTitle(text=f"{self.chart_title} (No Data)"),
                series=[]
            )

        # Use the inherited helper methods for data processing
        categories, values = self._process_time_series_data(metric_data)
        growth_rates = self._calculate_growth_rates(values)

        return ChartData(
            title=ChartTitle(text=self.chart_title),
            legend=ChartLegend(data=[self.series_name, "增长率"], bottom=2,left=150),
            xAxis=[ChartAxis(type="category", data=categories, name="", nameLocation="middle", nameGap=30, axisLabel={"show": False})],
            yAxis=[
                ChartAxis(type="value", axisLabel={"formatter": "{value}"}),
                ChartAxis(type="value", position="right", axisLabel={"formatter": "{value} %"})
            ],
            series=[
                ChartSeries(name=self.series_name, type="bar", data=values, label=value_label),
                ChartSeries(name="增长率", type="line", yAxisIndex=1, data=growth_rates, smooth=True, label=ratio_label),
            ]
        )

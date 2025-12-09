from abc import abstractmethod
from typing import List, Dict, Any
import pandas as pd
from .base_metric import BaseMetric, ratio_label, value_label
from schemas.chart import ChartData, ChartAxis, ChartSeries, ChartTitle, ChartLegend

class RatioMetric(BaseMetric):
    """
    Abstract base class for ratio-based metrics.
    It handles the common logic of fetching two dependent metrics (numerator and denominator),
    calculating the ratio, and generating chart data.

    Subclasses must define `metric_name`, `numerator_metric`, `denominator_metric`,
    and can override `chart_title`.
    """
    @property
    @abstractmethod
    def numerator_metric(self) -> str:
        """The metric name for the numerator."""
        raise NotImplementedError

    @property
    @abstractmethod
    def denominator_metric(self) -> str:
        """The metric name for the denominator."""
        raise NotImplementedError
        
    @property
    @abstractmethod
    def chart_title(self) -> str:
        """The title for the chart."""
        raise NotImplementedError

    @property
    def dependencies(self) -> List[str]:
        """Dependencies are automatically derived from numerator and denominator."""
        return [self.numerator_metric, self.denominator_metric]

    def get_chart_data(self, time_series_data: Dict[str, List[Dict[str, Any]]]) -> ChartData:
        """
        Calculates the ratio from the provided time series data for numerator and denominator.
        """
        numerator_data = time_series_data.get(self.numerator_metric)
        denominator_data = time_series_data.get(self.denominator_metric)

        if not numerator_data or not denominator_data:
            return ChartData(
                title=ChartTitle(text=f"{self.chart_title} (No Data)"),
                series=[]
            )

        # --- Data Processing ---
        df_num = pd.DataFrame(numerator_data).set_index("year")
        df_den = pd.DataFrame(denominator_data).set_index("year")

        # Align data by year and calculate the ratio
        # Replace 0 in denominator with NA to avoid division by zero, then fill resulting NaNs with 0
        df_ratio = (df_num["value"] / df_den["value"].replace(0, pd.NA)).dropna()
        
        if df_ratio.empty:
            return ChartData(
                title=ChartTitle(text=f"{self.chart_title} (No Data)"),
                series=[]
            )

        categories = df_ratio.index.tolist()
        values = df_ratio.round(2).tolist()
        growth_rates = self._calculate_growth_rates(values)

        return ChartData(
            title=ChartTitle(text=self.chart_title),
            legend=ChartLegend(data=["比率", "增长率"], right='right'),
            xAxis=[ChartAxis(type="category", data=categories, name="年份", nameLocation="middle", nameGap=30, axisLabel={"show": True})],
            yAxis=[
                ChartAxis(type="value", axisLabel={"formatter": "{value}"}),
                ChartAxis(type="value", position="right", axisLabel={"formatter": "{value} %"})
            ],
            series=[
                ChartSeries(name="比率", type="bar", data=values, label=value_label),
                ChartSeries(name="增长率", type="line", yAxisIndex=1, data=growth_rates, smooth=True, label=ratio_label),
            ]
        )

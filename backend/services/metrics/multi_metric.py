from abc import abstractmethod
from typing import List, Dict, Any
import pandas as pd
from .base_metric import BaseMetric, ratio_label, value_label
from schemas.chart import ChartData, ChartAxis, ChartSeries, ChartTitle, ChartLegend

class MultiMetric(BaseMetric):
    """
    Abstract base class for metrics that perform operations on multiple dependent metrics.
    It handles the common logic of fetching multiple dependent metrics,
    performing a defined operation, and generating chart data.

    Subclasses must define `metric_name`, `dependent_metrics`, `chart_title`,
    and implement `_calculate_series_values` to define the specific operation.
    """

    @property
    @abstractmethod
    def dependent_metrics(self) -> List[str]:
        """The list of metric names that this metric depends on."""
        raise NotImplementedError

    @property
    @abstractmethod
    def chart_title(self) -> str:
        """The title for the chart."""
        raise NotImplementedError

    @property
    def dependencies(self) -> List[str]:
        """Dependencies are automatically derived from the dependent_metrics list."""
        return self.dependent_metrics

    @abstractmethod
    def _calculate_series_values(self, aligned_df: pd.DataFrame) -> pd.Series:
        """
        Abstract method to define the specific operation on the dependent metrics.
        Takes a DataFrame where columns are dependent metric names and index is 'year'.
        Returns a pandas Series of the calculated values.
        """
        raise NotImplementedError

    def get_chart_data(self, time_series_data: Dict[str, List[Dict[str, Any]]]) -> ChartData:
        """
        Calculates the metric values from the provided time series data for dependent metrics.
        """
        # Fetch data for all dependent metrics and store in a dictionary
        dependent_dfs = {}
        for metric_name in self.dependent_metrics:
            data = time_series_data.get(metric_name)
            if not data:
                # If any dependent metric data is missing, we cannot calculate
                return ChartData(
                    title=ChartTitle(text=f"{self.chart_title} (No Data)"),
                    series=[]
                )
            dependent_dfs[metric_name] = pd.DataFrame(data).set_index("year")

        # Merge all dependent dataframes into a single dataframe, aligning by year
        # Use 'outer' join to keep all years, then fill NaNs if necessary (e.g., with 0)
        # The choice of fillna(0) depends on the specific operation.
        # For sum/average, 0 might be appropriate. For other operations, it might need adjustment.
        aligned_df = pd.DataFrame()
        for metric_name, df in dependent_dfs.items():
            aligned_df = aligned_df.merge(df["value"].rename(metric_name),
                                          left_index=True,
                                          right_index=True,
                                          how='outer')
        
        # Drop rows where any of the dependent metrics are NaN (meaning no data for that year)
        # Or, depending on the operation, you might want to fill NaNs.
        aligned_df = aligned_df.dropna()

        if aligned_df.empty:
            return ChartData(
                title=ChartTitle(text=f"{self.chart_title} (No Data)"),
                series=[]
            )

        # Calculate the series values using the abstract method defined by the subclass
        calculated_series = self._calculate_series_values(aligned_df)
        
        if calculated_series.empty:
            return ChartData(
                title=ChartTitle(text=f"{self.chart_title} (No Data)"),
                series=[]
            )

        categories = calculated_series.index.tolist()
        values = calculated_series.round(2).tolist()
        growth_rates = self._calculate_growth_rates(values)

        return ChartData(
            title=ChartTitle(text=self.chart_title),
            legend=ChartLegend(data=["值", "增长率"], right='right'),
            xAxis=[ChartAxis(type="category", data=categories, name="年份", nameLocation="middle", nameGap=30, axisLabel={"show": True})],
            yAxis=[
                ChartAxis(type="value", axisLabel={"formatter": "{value}"}),
                ChartAxis(type="value", position="right", axisLabel={"formatter": "{value} %"})
            ],
            series=[
                ChartSeries(name="值", type="bar", data=values, label=value_label),
                ChartSeries(name="增长率", type="line", yAxisIndex=1, data=growth_rates, smooth=True, label=ratio_label),
            ]
        )

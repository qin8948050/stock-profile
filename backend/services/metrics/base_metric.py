from abc import ABC, abstractmethod
from typing import List, Dict, Any
from schemas.chart import ChartData, ChartAxis, ChartSeries, ChartTitle, ChartLegend

ratio_label={
    "show": True,
    "position": "top",
    "formatter": "{c}%",
    "color": "#ffffff",  # 纯白色，最清晰
    "fontSize": 14,      # 字体调大（关键）
    "fontWeight": "bold",

    # 加粗边框，增强对比度
    "textBorderColor": "rgba(0,0,0,0.8)",
    "textBorderWidth": 3,

    # 微弱阴影，让白字更立体
    "textShadowColor": "rgba(0,0,0,0.4)",
    "textShadowBlur": 4,
}
lineStyle={
    "width": 3
}
itemStyle={
    "color": "#C0C000"    # 黄绿色点
}

value_label={"show": True, "position": "inside",     "fontSize": 14,"formatter": "{c}"}

class BaseMetric(ABC):
    """
    Abstract base class for defining a financial metric's chart configuration.
    """
    metric_name: str = "base_metric"

    @abstractmethod
    def get_chart_data(self, time_series_data: List[Dict[str, Any]]) -> ChartData:
        """
        Generates the ChartData object for the metric using the provided time series data.
        """
        raise NotImplementedError

    def _calculate_growth_rates(self, values: List[float]) -> List[float]:
        """
        Helper method to calculate year-over-year growth rates.
        Can be overridden by subclasses if a different calculation is needed.
        """
        growth_rates = [0.0]
        for i in range(1, len(values)):
            prev = values[i-1]
            curr = values[i]
            rate = ((curr - prev) / abs(prev)) * 100 if prev and prev != 0 else 0
            growth_rates.append(round(rate, 2))
        return growth_rates


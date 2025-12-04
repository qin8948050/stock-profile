from typing import List, Optional, Union, Dict, Any, Literal
from pydantic import BaseModel, Field

class ChartTitle(BaseModel):
    text: Optional[str] = None

class ChartLegend(BaseModel):
    data: List[str] = []
    top: Optional[str] =None
    left: Optional[str] =None
    right: Optional[str] =None
    bottom: Optional[str]=None

class ChartAxis(BaseModel):
    type: str
    name: Optional[str] = None
    data: Optional[List[str]] = None
    min: Optional[Union[int, str]] = None
    max: Optional[Union[int, str]] = None
    position: Optional[str] = None
    axis_label: Optional[Dict[str, Any]] = Field(None, alias="axisLabel")
    name_location: Optional[str] = Field(None, alias="nameLocation")
    name_gap: Optional[int] = Field(None, alias="nameGap")

class ChartSeries(BaseModel):
    name: str
    type: str
    data: List[Union[float, int]]
    y_axis_index: Optional[int] = Field(None, alias="yAxisIndex")
    smooth: Optional[bool] = None
    bar_width: Optional[str] = Field('40%', alias="barWidth")
    label: Optional[Dict[str, Any]] = None # Added label field

class ChartData(BaseModel):
    title: ChartTitle = Field(default_factory=ChartTitle)
    legend: ChartLegend = Field(default_factory=ChartLegend)
    x_axis: List[ChartAxis] = Field([], alias="xAxis")
    y_axis: List[ChartAxis] = Field([], alias="yAxis")
    series: List[ChartSeries] = []

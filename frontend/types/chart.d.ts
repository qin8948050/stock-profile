export interface ChartTitle {
    text?: string;
}

export interface ChartLegend {
    data: string[];
    top?: (string|number);
    left?: (string|number);
    right?: (string|number);
    bottom?: (string|number);
}

export interface ChartAxis {
    type: string;
    name?: string;
    data?: string[];
    min?: number | string;
    max?: number | string;
    position?: string;
    axisLabel?: Record<string, any>;
    nameLocation?: string;
    nameGap?: number;
}

export interface ChartSeries {
    name: string;
    type: string;
    data: (number | string)[];
    yAxisIndex?: number;
    smooth?: boolean;
    barWidth?: string;
    label?: Record<string, any>;
}

export interface ChartData {
    title: ChartTitle;
    legend: ChartLegend;
    xAxis: ChartAxis[];
    yAxis: ChartAxis[];
    series: ChartSeries[];
}

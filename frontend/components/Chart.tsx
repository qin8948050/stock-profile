import { FC, HTMLAttributes, useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';
import { Spin } from 'antd';
import { merge } from 'lodash';

interface ChartProps extends HTMLAttributes<HTMLDivElement> {
  getData: (params?: any) => Promise<any>; // Modified to accept params
  params?: any; // New prop for passing parameters to getData
}

const DEFAULT_GRID_CONFIG = {
  grid: {
    left: '3%',
    right: '4%',
    bottom: '10%', // Default bottom for legend
    containLabel: true,
  },
};

const DEFAULT_TOOLTIP_CONFIG = {
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' },
    formatter: (params: any[]) => {
      const valueParam = params.find(p => p.seriesName === '数值');
      const rateParam = params.find(p => p.seriesName === '增长率');
      if (!valueParam || !rateParam) return '';
      
      const category = valueParam.name;
      const value = valueParam.value ? Number(valueParam.value).toFixed(2) : 'N/A';
      const rate = rateParam.value ? Number(rateParam.value).toFixed(2) : 'N/A';

      return `${category}<br/>${valueParam.seriesName}: ${value}<br/>${rateParam.seriesName}: ${rate}%`;
    }
  },
};

const DEFAULT_TITLE_CONFIG = {
  title: {
    left: 'center',
    textStyle: {
      fontSize: 14,
    }
  }
};

const Chart: FC<ChartProps> = ({ getData, params, ...rest }) => { // Added params to destructuring
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    if (chartRef.current) {
      chartInstance.current = echarts.init(chartRef.current);
    }

    const loadData = async () => {
      setLoading(true);
      try {
        const fetchedOption = await getData(params); // Pass params to getData
        if (isMounted && chartInstance.current) {
          // Merge the fetched option with our default title, grid and tooltip config
          const finalOption = merge({}, DEFAULT_TITLE_CONFIG, DEFAULT_TOOLTIP_CONFIG, DEFAULT_GRID_CONFIG, fetchedOption);
          chartInstance.current.setOption(finalOption);
        }
      } catch (error) {
        console.error("Failed to fetch chart data:", error);
        // You could display an error message here
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadData();

    // Handle component unmount
    return () => {
      isMounted = false;
      chartInstance.current?.dispose();
    };
  }, [getData, params]); // Added params to dependency array

  // Resize chart with window
  useEffect(() => {
    const handleResize = () => {
      chartInstance.current?.resize();
    };
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', ...rest.style }}>
      {loading && (
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Spin />
        </div>
      )}
      <div ref={chartRef} {...rest} style={{ visibility: loading ? 'hidden' : 'visible', height: '100%', width: '100%' }} />
    </div>
  );
};

export default Chart;

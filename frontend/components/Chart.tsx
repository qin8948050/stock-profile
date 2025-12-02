import { FC, HTMLAttributes, useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';
import { Spin } from 'antd';
import { merge } from 'lodash';

interface ChartProps extends HTMLAttributes<HTMLDivElement> {
  getData: () => Promise<any>;
}

const DEFAULT_GRID_CONFIG = {
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
};

const Chart: FC<ChartProps> = ({ getData, ...rest }) => {
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
        const fetchedOption = await getData();
        if (isMounted && chartInstance.current) {
          // Merge the fetched option with our default grid config
          const finalOption = merge({}, DEFAULT_GRID_CONFIG, fetchedOption);
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
  }, [getData]);

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

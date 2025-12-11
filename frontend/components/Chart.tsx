import { FC, HTMLAttributes, useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';
import { Spin, Modal } from 'antd';
import { merge } from 'lodash';
import { getFinancialMetric } from '../lib/financialApi';

interface ChartProps extends HTMLAttributes<HTMLDivElement> {
  companyId: number;
  metricName: string;
}

const DEFAULT_GRID_CONFIG = {
  grid: {
    left: '3%',
    right: '4%',
    bottom: '20%',
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

const Chart: FC<ChartProps> = ({ companyId, metricName, ...rest }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);
  const [loading, setLoading] = useState(true);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [chartOption, setChartOption] = useState<any>(null);

  const modalChartRef = useRef<HTMLDivElement>(null);
  const modalChartInstance = useRef<echarts.ECharts | null>(null);

  // Effect for the main chart
  useEffect(() => {
    let isMounted = true;
    if (chartRef.current) {
      chartInstance.current = echarts.init(chartRef.current);
    }

    const loadData = async () => {
      setLoading(true);
      try {
        const fetchedOption = await getFinancialMetric(companyId, metricName);
        if (isMounted) {
          const finalOption = merge({}, DEFAULT_TITLE_CONFIG, DEFAULT_TOOLTIP_CONFIG, DEFAULT_GRID_CONFIG, fetchedOption);
          setChartOption(finalOption);
          if (chartInstance.current) {
            chartInstance.current.setOption(finalOption);
          }
        }
      } catch (error) {
        console.error("Failed to fetch chart data:", error);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadData();

    return () => {
      isMounted = false;
      chartInstance.current?.dispose();
    };
  }, [companyId, metricName]);

  // Resize main chart with window
  useEffect(() => {
    const handleResize = () => {
      chartInstance.current?.resize();
    };
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // Function to handle modal opening and initialize the modal chart
  const handleModalAfterOpen = () => {
    if (modalChartRef.current && chartOption) {
      modalChartInstance.current = echarts.init(modalChartRef.current);
      modalChartInstance.current.setOption(chartOption);
      modalChartInstance.current.resize(); // Ensure it resizes to modal's dimensions

      const handleModalResize = () => {
        modalChartInstance.current?.resize();
      };
      window.addEventListener('resize', handleModalResize);

      // Cleanup function for modal chart
      const cleanupModalChart = () => {
        modalChartInstance.current?.dispose();
        modalChartInstance.current = null;
        window.removeEventListener('resize', handleModalResize);
      };
      // Store cleanup function to be called when modal closes
      (modalChartRef.current as any).cleanup = cleanupModalChart;
    }
  };

  const handleModalClose = () => {
    setIsModalVisible(false);
    // Call cleanup function if it exists
    if (modalChartRef.current && (modalChartRef.current as any).cleanup) {
      (modalChartRef.current as any).cleanup();
    }
  };

  const handleChartClick = () => {
    setIsModalVisible(true);
  };

  return (
    <>
      <div
        style={{ position: 'relative', width: '100%', height: '100%', cursor: 'pointer', ...rest.style }}
        onClick={handleChartClick}
      >
        {loading && (
          <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <Spin />
          </div>
        )}
        <div ref={chartRef} {...rest} style={{ visibility: loading ? 'hidden' : 'visible', height: '100%', width: '100%' }} />
      </div>

      <Modal
        title={chartOption?.title?.text || "Chart Detail"}
        open={isModalVisible}
        onCancel={handleModalClose}
        footer={null}
        width="80%"
        destroyOnClose
        afterOpenChange={(open) => {
          if (open) {
            handleModalAfterOpen();
          }
        }}
      >
        {chartOption && (
          <div ref={modalChartRef} style={{ height: '60vh', width: '100%' }} />
        )}
      </Modal>
    </>
  );
};

export default Chart;

import { FC } from 'react';
import { Row, Col } from 'antd';
import Chart from './Chart';

interface ChartGridProps {
  /**
   * An array of functions, where each function returns a promise that resolves to an ECharts option object.
   */
  chartGetters: (() => Promise<any>)[];
  /**
   * The height of each chart container.
   * @default '300px'
   */
  chartHeight?: string | number;
}

/**
 * A responsive grid for displaying multiple charts.
 * It arranges charts in a grid that adapts to screen size (up to 4 charts per row on large screens).
 */
const ChartGrid: FC<ChartGridProps> = ({ chartGetters, chartHeight = '300px' }) => {
  if (!chartGetters || chartGetters.length === 0) {
    return <p>No charts to display.</p>;
  }

  return (
    <Row gutter={[16, 16]}>
      {chartGetters.map((getData, index) => (
        <Col key={index} xs={24} sm={12} md={12} lg={8} xl={6}>
          <div style={{ height: chartHeight, border: '1px solid #f0f0f0', borderRadius: '8px', padding: '8px' }}>
            <Chart getData={getData} />
          </div>
        </Col>
      ))}
    </Row>
  );
};

export default ChartGrid;

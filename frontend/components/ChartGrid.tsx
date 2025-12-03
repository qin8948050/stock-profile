import { FC } from 'react';
import { Row, Col } from 'antd';
import Chart from './Chart';

interface ChartItem {
  getData: (params?: any) => Promise<any>;
  params?: any;
}

interface ChartGridProps {
  /**
   * An array of chart items, where each item contains a getData function and optional parameters.
   */
  chartItems: ChartItem[]; // Renamed from chartGetters
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
const ChartGrid: FC<ChartGridProps> = ({ chartItems, chartHeight = '300px' }) => { // Renamed prop
  if (!chartItems || chartItems.length === 0) {
    return <p>No charts to display.</p>;
  }

  return (
    <Row gutter={[16, 16]}>
      {chartItems.map((chartItem, index) => ( // Iterate over chartItems
        <Col key={index} xs={24} sm={12} md={12} lg={8} xl={6}>
          <div style={{ height: chartHeight, border: '1px solid #f0f0f0', borderRadius: '8px', padding: '8px' }}>
            <Chart getData={chartItem.getData} params={chartItem.params} /> {/* Pass getData and params */}
          </div>
        </Col>
      ))}
    </Row>
  );
};

export default ChartGrid;

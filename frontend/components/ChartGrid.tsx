import { FC } from 'react';
import { Row, Col } from 'antd';
import Chart from './Chart';

interface ChartGridProps {
  chartItems: string[];
  companyId: number;
  chartHeight?: string | number;
}

const ChartGrid: FC<ChartGridProps> = ({ chartItems, companyId, chartHeight = '300px' }) => {
  if (!chartItems || chartItems.length === 0) {
    return <p>No charts to display.</p>;
  }

  return (
    <Row gutter={[16, 16]}>
      {chartItems.map((metricName, index) => (
        <Col key={index} xs={24} sm={12} md={12} lg={8} xl={6}>
          <div style={{ height: chartHeight, border: '1px solid #f0f0f0', borderRadius: '8px', padding: '8px' }}>
            <Chart companyId={companyId} metricName={metricName} />
          </div>
        </Col>
      ))}
    </Row>
  );
};

export default ChartGrid;

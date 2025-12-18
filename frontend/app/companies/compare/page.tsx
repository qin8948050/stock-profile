"use client";

import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Table, Spin, Alert, Button } from 'antd';
import { fetchCompany } from '../../../lib/companyApi';
import type { Company } from '../../../types/company';
import Link from 'next/link';

const ComparePage = () => {
  const searchParams = useSearchParams();
  const ids = searchParams.get('ids');
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const companyIds = ids ? ids.split(',').map(id => parseInt(id, 10)) : [];
    if (companyIds.length > 0) {
      setLoading(true);
      Promise.all(companyIds.map(id => fetchCompany(id)))
        .then(data => {
          setCompanies(data);
          setLoading(false);
        })
        .catch(err => {
          setError('加载公司信息失败');
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, [ids]);

  if (loading) {
    return <Spin tip="加载中..." style={{ display: 'block', marginTop: 50 }} />;
  }

  if (error) {
    return <Alert message="错误" description={error} type="error" showIcon />;
  }

  const comparisonColumns = [
    { title: '属性', dataIndex: 'property', key: 'property', width: 150, fixed: 'left' as 'left' },
    ...companies.map((company, index) => ({
      title: company.name,
      dataIndex: `company${index}`,
      key: `company${index}`,
      width: 200,
    }))
  ];

  const comparisonDataSource = [
    { property: '代码', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.ticker])) },
    { property: '主营业务', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.main_business])) },
    { property: '员工数', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.employee_count])) },
    { property: '市场地位', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.market_position])) },
    { property: '差异化', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.differentiation])) },
    { property: '供应链控制', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.supply_chain_control])) },
    { property: '行业分类', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.industry_profile?.industry_category])) },
    { property: '行业规模', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.industry_profile?.industry_size])) },
    { property: '集中度', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.industry_profile?.concentration_level])) },
    { property: '行业壁垒', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.industry_profile?.industry_barrier])) },
    { property: '5年复合增长率', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.industry_profile?.industry_cagr_5y])) },
    { property: '主要竞争对手', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.industry_profile?.major_competitors])) },
    { property: '行业趋势', ...Object.fromEntries(companies.map((c, i) => [`company${i}`, c.industry_profile?.industry_trend])) },
  ];

  return (
    <main style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h1>公司比较</h1>
        <Link href={`/companies?selected=${ids || ''}`}>
          <Button type="primary">返回公司列表</Button>
        </Link>
      </div>
      <Table
        rowKey="property"
        columns={comparisonColumns}
        dataSource={comparisonDataSource}
        pagination={false}
        bordered
        scroll={{ x: 'max-content' }}
      />
    </main>
  );
};

export default ComparePage;

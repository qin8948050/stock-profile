"use client"
import {OrganizationChart, OrganizationChartOptions} from '@ant-design/graphs';
import { Spin } from 'antd';
import { useEffect, useState } from 'react';
import { fetchCompany } from '../../../lib/api';
import { Company } from '../../../types/company';

interface BusinessTabProps {
    companyId: number;
}

export default function BusinessTab({ companyId }: BusinessTabProps) {
    const [company, setCompany] = useState<Company | null>(null);
    const [loading, setLoading] = useState(true);
    const [jsonData, setJsonData] = useState();

    useEffect(() => {
        fetch('https://assets.antv.antgroup.com/g6/organization-chart.json')
            .then((res) => res.json())
            .then(setJsonData);
    }, []);

    useEffect(() => {
        if (companyId) {
            setLoading(true);
            fetchCompany(companyId)
                .then(setCompany)
                .catch(() => setCompany(null))
                .finally(() => setLoading(false));
        }
    }, [companyId]);

    if (loading) {
        return (
            <div
                style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '100vh',
                }}
            >
                <Spin size="large" />
            </div>
        );
    }

    if (!company) {
        return <div>Failed to load company data.</div>;
    }


    const data = {
        id: String(company.id),
        value: {
            name: company.name,
            ticker: company.ticker,
            main_business: company.main_business,
            employee_count: company.employee_count,
            market_position: company.market_position,
            differentiation: company.differentiation,
            supply_chain_control: company.supply_chain_control,
        },
        children: [
            {
                id: `${company.id}-industry`,
                value: {
                    name: 'Industry Profile',
                    ...company.industry_profile,
                },
            },
        ],
    };

    const config = {
        data,
        nodeCfg: {
            autoWidth: true,
            items: {
                layout: 'follow',
            },
            title: {
                style: {
                    fill: '#fff',
                },
            },
            style: (node: any) => {
                if (node.children) {
                    return {
                        fill: '#3f51b5',
                        stroke: '#3f51b5',
                    };
                }
                return {
                    fill: '#f50057',
                    stroke: '#f50057',
                };
            },
        },
        edgeCfg: {
            style: {
                stroke: '#3f51b5',
            },
        },
        markerCfg: (cfg: any) => {
            const { children } = cfg;
            return {
                show: children?.length,
            };
        },
        behaviors: ['drag-canvas', 'zoom-canvas', 'drag-node'],
    };

    const options: OrganizationChartOptions = {
        autoFit: 'view',
        data:jsonData,
        labelField: 'name',
    };

    return <OrganizationChart {...options} />;
}
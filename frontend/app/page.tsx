"use client";

import React, { useEffect, useState } from "react";
import { Card, Typography, Row, Col, Button, Space, Statistic, message } from "antd";
import Link from "next/link";
import { fetchCompanies } from "../lib/api";
import { PaginatedCompanies } from "@/types/company";


const { Title, Paragraph } = Typography;

export default function Home() {
  const [companyCount, setCompanyCount] = useState<number | null>(null);

  useEffect(() => {
    fetchCompanies({
      page: 1,
      size: 1,
    })
      .then((data) => {
        // API returns array of companies; get total via length if limited
        // If backend supports a total field later, we can switch to that.
        setCompanyCount(data.total);
      })
      .catch((e) => {
        // message.warn is not in AntD message types in some versions; use notify.error for compatibility
        // import notify lazily to avoid changing top-level imports for this small change
        const { default: notify } = require("../utils/notify");
        notify.error(e, "无法获取公司数据：");
        setCompanyCount(null);
      });
  }, []);

  return (
    <main style={{ padding: 24 }}>
      <section>
        <Row gutter={16} align="middle">
        <Col span={16}>
          <Title level={2}>欢迎来到 Stock Profile</Title>
          <Paragraph style={{ fontSize: 16 }}>
            这是一个股票/公司画像管理工具。你可以在此查看公司列表、查看或编辑公司信息，和管理行业画像。
          </Paragraph>
          <Space style={{ marginTop: 12 }}>
            <Link href="/companies">
              <Button type="primary">查看公司</Button>
            </Link>
            <Link href="/companies">
              <Button>管理公司</Button>
            </Link>
          </Space>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="公司数量（示例）" value={companyCount ?? "—"} />
            <div style={{ marginTop: 12 }}>
              <Link href="/companies">
                <Button>转到公司列表</Button>
              </Link>
            </div>
          </Card>
        </Col>
      </Row>  
      </section>


      <section style={{ marginTop: 24 }}>
        <Row>
          <Col span={24}>
            <Card title="快速提示">
              <ul>
                <li>公司数据来自后端 API（路径：/api/companies）。</li>
                <li>可通过右上角导航进入公司列表和详情。</li>
                <li>如需增加行业画像字段，请在“新建/编辑”页面完善。</li>
              </ul>
            </Card>
          </Col>
        </Row>
      </section>
    </main>
  );
}

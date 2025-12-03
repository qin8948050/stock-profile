"use client";

import React, { useState } from "react";
import { Card, Select, Upload, Button, Form, Modal } from "antd";
import { AntDesignOutlined, UploadOutlined } from "@ant-design/icons";
import notify from "../../../utils/notify";
import { uploadFinancialStatement } from "../../../lib/financialApi";
import GradientButton from "@/components/Buttons";
import ChartGrid from "@/components/ChartGrid";

interface FinancialTabProps {
  companyId: number;
}

const STATEMENT_TYPE_OPTIONS = [
  { label: "利润表 (Income Statement)", value: "income" },
  { label: "资产负债表 (Balance Sheet)", value: "balance" },
  { label: "现金流量表 (Cash Flow Statement)", value: "cash" },
];

// Mock data fetching from backend with more details
// Now accepts chartParams to customize the chart
const getChartData = async (chartParams?: { title: string }) => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // 1. Generate base data
  const categories = ['2018', '2019', '2020', '2021', '2022', '2023', '2024'];
  const values = Array.from({ length: 7 }, () => Math.floor(Math.random() * 500) + 800);

  // 2. Calculate growth rate
  const growthRates = [0]; // Growth rate for the first year is 0
  for (let i = 1; i < values.length; i++) {
    const previous = values[i - 1];
    const current = values[i];
    const rate = previous === 0 ? 0 : ((current - previous) / previous) * 100;
    growthRates.push(rate);
  }

  return {
    title: { // Title now comes from chartParams
      text: chartParams?.title,
    },
    legend: {
      data: ['数值', '增长率'],
      top: 'bottom' // Keep legend at bottom
    },
    // Removed grid and tooltip as they are now handled by Chart.tsx defaults
    xAxis: [
      {
        type: 'category',
        data: categories,
        name: '年度',
        nameLocation: 'middle',
        nameGap: 22,
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: '数值 (万元)',
        min: 0,
        axisLabel: { formatter: '{value}' }
      },
      {
        type: 'value',
        name: '增长率',
        min: -50,
        max: 50,
        position: 'right',
        axisLabel: { formatter: '{value} %' }
      }
    ],
    series: [
      {
        name: '数值',
        type: 'bar',
        yAxisIndex: 0,
        data: values,
      },
      {
        name: '增长率',
        type: 'line',
        yAxisIndex: 1,
        data: growthRates,
        smooth: true,
      }
    ]
  };
};

export default function FinancialTab({ companyId }: FinancialTabProps) {
  const [form] = Form.useForm();
  const [uploading, setUploading] = useState(false);
  const [fileList, setFileList] = useState<any[]>([]);
  const [isModalVisible, setIsModalVisible] = useState(false);

  // For demonstration, create an array of chart items with different titles
  const chartItems = [
    { getData: getChartData, params: { title: '总收入分析' } },
    { getData: getChartData, params: { title: '净利润趋势' } },
    { getData: getChartData, params: { title: '现金流概览' } },
    { getData: getChartData, params: { title: '资产负债变化' } },
  ];

  const handleUpload = async (values: { statementType: string }) => {
    if (fileList.length === 0) {
      notify.error("请先选择一个文件。");
      return;
    }

    const { statementType } = values;
    const file = fileList[0];

    setUploading(true);

    try {
      await uploadFinancialStatement({
        company_id: companyId,
        type: statementType,
        file: file,
      });
      notify.success("上传成功");
      setIsModalVisible(false);
      form.resetFields();
      setFileList([]);
    } catch (err: any) {
      notify.error(err, "上传失败");
    } finally {
      setUploading(false);
    }
  };

  const props = {
    onRemove: (file: any) => {
      setFileList([]);
    },
    beforeUpload: (file: any) => {
      if (file.type !== "application/json") {
        notify.error("只能上传 JSON 文件！");
        return Upload.LIST_IGNORE;
      }
      setFileList([file]);
      return false; // Prevent auto-upload
    },
    fileList,
    maxCount: 1,
  };

  return (
    <>
      <Card
        title="财务报表分析"
        extra={
          <GradientButton size="middle" type="primary" icon={<AntDesignOutlined />} onClick={() => setIsModalVisible(true)}>上传财报</GradientButton>
        }
      >
        <ChartGrid chartItems={chartItems} chartHeight={350} />
      </Card>
      <Modal
        title="上传财务报表"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        destroyOnClose
      >
        <Form form={form} onFinish={handleUpload} layout="vertical" style={{ marginTop: 24 }}>
          <Form.Item
            name="statementType"
            label="财务报表类型"
            rules={[{ required: true, message: "请选择报表类型！" }]}
          >
            <Select
              placeholder="请选择要上传的财务报表类型"
              options={STATEMENT_TYPE_OPTIONS}
            />
          </Form.Item>

          <Form.Item label="上传数据文件" required>
            <Upload {...props}>
              <Button icon={<UploadOutlined />}>选择 JSON 文件</Button>
            </Upload>
            </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={uploading}
              disabled={fileList.length === 0}
            >
              {uploading ? "正在上传..." : "开始上传"}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}

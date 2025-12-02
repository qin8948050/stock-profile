"use client";

import React, { useState } from "react";
import { Card, Select, Upload, Button, Form, Modal } from "antd";
import { AntDesignOutlined, UploadOutlined } from "@ant-design/icons";
import notify from "../../../utils/notify";
import { uploadFinancialStatement } from "../../../lib/financialApi";
import GradientButton from "@/components/Buttons";
import ChartGrid from "@/components/ChartGrid"; // Import the new ChartGrid component

interface FinancialTabProps {
  companyId: number;
}

const STATEMENT_TYPE_OPTIONS = [
  { label: "利润表 (Income Statement)", value: "income" },
  { label: "资产负债表 (Balance Sheet)", value: "balance" },
  { label: "现金流量表 (Cash Flow Statement)", value: "cash" },
];

// Mock data fetching from backend
const getChartData = async () => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  const randomData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 500) + 800);
  console.log(randomData)
  return {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: randomData,
      type: 'line'
    }]
  };
};

export default function FinancialTab({ companyId }: FinancialTabProps) {
  const [form] = Form.useForm();
  const [uploading, setUploading] = useState(false);
  const [fileList, setFileList] = useState<any[]>([]);
  const [isModalVisible, setIsModalVisible] = useState(false);

  // For demonstration, let's create an array of getData functions for multiple charts
  const chartGetters = Array.from({ length: 4 }).map(() => getChartData);

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
        <ChartGrid chartGetters={chartGetters} chartHeight={300} />
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

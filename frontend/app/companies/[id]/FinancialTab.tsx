"use client";

import React, { useState } from "react";
import { Card, Select, Upload, Button, Form, Modal } from "antd";
import { AntDesignOutlined, UploadOutlined } from "@ant-design/icons";
import notify from "../../../utils/notify";
import { uploadFinancialStatement } from "../../../lib/financialApi";
import GradientButton from "@/components/Buttons";
import ChartGrid, {ChartItem} from "@/components/ChartGrid";

interface FinancialTabProps {
  companyId: number;
}

const STATEMENT_TYPE_OPTIONS = [
  { label: "利润表 (Income Statement)", value: "income" },
  { label: "资产负债表 (Balance Sheet)", value: "balance" },
  { label: "现金流量表 (Cash Flow Statement)", value: "cash" },
];

export default function FinancialTab({ companyId }: FinancialTabProps) {
  const [form] = Form.useForm();
  const [uploading, setUploading] = useState(false);
  const [fileList, setFileList] = useState<any[]>([]);
  const [isModalVisible, setIsModalVisible] = useState(false);

  // Add metric list
  const chartItems: ChartItem[] = [
    { metricName: 'total_assets' },
    { metricName: 'total_liabilities' },
    { metricName: 'cash_at_end_of_period' },
    { metricName: 'asset_liability_ratio' },
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
        <ChartGrid chartItems={chartItems} companyId={companyId} chartHeight={350} />
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

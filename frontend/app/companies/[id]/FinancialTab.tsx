"use client";

import React, { useState } from "react";
import { Card, Select, Upload, Button, Form, Space } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import notify from "../../../utils/notify";
import { uploadFinancialStatement } from "../../../lib/financialApi";
import {deleteCompany} from "@/lib/companyApi";

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
              company: companyId,
              type: statementType,
              file: file,
          });
          notify.success("上传成功");
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
    <Card>
      <Form form={form} onFinish={handleUpload} layout="vertical">
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

        <Form.Item
          label="上传数据文件"
          rules={[{ required: true, message: "请选择一个文件！" }]}
        >
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
    </Card>
  );
}
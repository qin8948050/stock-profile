"use client";

import React, { useEffect, useState } from "react";
import {
  Card,
  Descriptions,
  Form,
  Input,
  InputNumber,
  Button,
  Space,
  Select,
  Row,
  Col,
  Upload,
} from "antd";
import { UploadOutlined } from "@ant-design/icons";
import notify from "../../../utils/notify";
import ActionBar from "../../../components/ActionBar";
import { fetchCompany, updateCompany } from "../../../lib/api";
import type { Company } from "../../../types/company";
import {
  CONCENTRATION_OPTIONS,
  BARRIER_OPTIONS,
  INDUSTRY_CATEGORY_OPTIONS,
  getLabel,
  normalizeCompanyForForm,
} from "./options";

const { TextArea } = Input;

interface ProfileTabProps {
  companyId: number;
}

export default function ProfileTab({ companyId }: ProfileTabProps) {
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [form] = Form.useForm();

  const loadCompany = () => {
    if (!companyId) return;
    setLoading(true);
    fetchCompany(companyId)
      .then((c) => {
        const normalized = normalizeCompanyForForm(c);
        setCompany(normalized);
        form.setFieldsValue(normalized);
      })
      .catch((e) => notify.error(e, "加载失败"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
      // eslint-disable-next-line react-hooks/set-state-in-effect
    loadCompany();
  }, [companyId]);

  const onFinish = async (values: any) => {
    // API expects nested structure
    const payload = {
      ...values,
      industry_profile: {
        ...(company?.industry_profile || {}),
        ...values.industry_profile,
      },
    };

    try {
      const updated = await updateCompany(companyId, payload);
      const normalized = normalizeCompanyForForm(updated);
      setCompany(normalized);
      form.setFieldsValue(normalized);
      notify.success("保存成功");
      setEditing(false);
    } catch (e: any) {
      notify.error(e, "保存失败");
    }
  };
  

  if (!company) {
    return <Card loading={true}>加载中...</Card>;
  }

  return (
    <Card>
      {!editing ? (
        <>
          <Descriptions column={2} bordered>
            <Descriptions.Item label="ID">{company.id}</Descriptions.Item>
            <Descriptions.Item label="代码">
              {company.ticker || "-"}
            </Descriptions.Item>
            <Descriptions.Item label="主营业务" span={2}>
              {company.main_business || "-"}
            </Descriptions.Item>
            <Descriptions.Item label="员工数">
              {company.employee_count || "-"}
            </Descriptions.Item>
            <Descriptions.Item label="行业分类">
              {getLabel(
                company.industry_profile?.industry_category,
                INDUSTRY_CATEGORY_OPTIONS
              ) || "-"}
            </Descriptions.Item>
            <Descriptions.Item label="行业规模(亿)">
              {company.industry_profile?.industry_size ?? "-"}
            </Descriptions.Item>
            <Descriptions.Item label="集中度">
              {getLabel(
                company.industry_profile?.concentration_level,
                CONCENTRATION_OPTIONS
              ) || "-"}
            </Descriptions.Item>
            <Descriptions.Item label="行业壁垒">
              {getLabel(
                company.industry_profile?.industry_barrier,
                BARRIER_OPTIONS
              ) || "-"}
            </Descriptions.Item>
            <Descriptions.Item label="行业 5 年 CAGR">
              {company.industry_profile?.industry_cagr_5y ?? "-"}
            </Descriptions.Item>
            <Descriptions.Item label="主要竞争者" span={2}>
              {company.industry_profile?.major_competitors || "-"}
            </Descriptions.Item>
            <Descriptions.Item label="行业趋势" span={2}>
              {company.industry_profile?.industry_trend || "-"}
            </Descriptions.Item>
          </Descriptions>
          <ActionBar>
            <Button type="primary" onClick={() => setEditing(true)}>
              编辑
            </Button>
          </ActionBar>
        </>
      ) : (
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={company}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="公司名称"
                rules={[{ required: true }]}
              >
                <Input />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="ticker" label="代码">
                <Input />
              </Form.Item>
            </Col>
            <Col span={24}>
              <Form.Item name="main_business" label="主营业务">
                <TextArea rows={3} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="employee_count" label="员工数">
                <InputNumber style={{ width: "100%" }} />
              </Form.Item>
            </Col>
          </Row>

          <fieldset
            style={{
              border: "1px solid #d9d9d9",
              borderRadius: 6,
              padding: "12px 16px",
              marginTop: 16,
            }}
          >
            <legend style={{ padding: "0 8px", marginLeft: 12, width: "auto", fontSize: 16 }}>
              行业信息
            </legend>
            <Row gutter={16}>
              <Col span={12}>
                <Form.Item
                  name={["industry_profile", "industry_category"]}
                  label="行业分类"
                >
                  <Select
                    options={INDUSTRY_CATEGORY_OPTIONS}
                    allowClear
                    placeholder="请选择行业分类"
                  />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item
                  name={["industry_profile", "industry_size"]}
                  label="行业规模(亿)"
                >
                  <InputNumber
                    style={{ width: "100%" }}
                    formatter={(value) =>
                      `¥ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ",")
                    }
                  />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item
                  name={["industry_profile", "concentration_level"]}
                  label="集中度"
                >
                  <Select
                    options={CONCENTRATION_OPTIONS}
                    allowClear
                    placeholder="请选择集中度"
                  />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item
                  name={["industry_profile", "industry_barrier"]}
                  label="行业壁垒"
                >
                  <Select
                    options={BARRIER_OPTIONS}
                    allowClear
                    placeholder="请选择行业壁垒"
                  />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item
                  name={["industry_profile", "industry_cagr_5y"]}
                  label="行业 5 年 CAGR (%)"
                >
                  <InputNumber style={{ width: "100%" }} addonAfter="%" />
                </Form.Item>
              </Col>
              <Col span={24}>
                <Form.Item
                  name={["industry_profile", "major_competitors"]}
                  label="主要竞争者"
                >
                  <TextArea rows={2} />
                </Form.Item>
              </Col>
              <Col span={24}>
                <Form.Item
                  name={["industry_profile", "industry_trend"]}
                  label="行业趋势"
                >
                  <TextArea rows={3} />
                </Form.Item>
              </Col>
            </Row>
          </fieldset>

          <ActionBar>
            <Space>
              <Button onClick={() => setEditing(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                保存
              </Button>
            </Space>
          </ActionBar>
        </Form>
      )}
    </Card>
  );
}
"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, Descriptions, Form, Input, InputNumber, Button, Space, Select } from "antd";
import notify from "../../../utils/notify";
import ActionBar from "../../../components/ActionBar";
import { fetchCompany, updateCompany } from "../../../lib/api";
import type { Company } from "../../../types/company";

export default function CompanyDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params?.id || 0);

  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [form] = Form.useForm();

  // Options for enum-like fields. Adjust values to match backend enum values.
  // Options for enum-like fields. Use backend enum NAMES as `value` and human labels as `label`.
  const CONCENTRATION_OPTIONS = [
    { label: "高度集中", value: "高度集中" },
    { label: "中等集中", value: "中等集中" },
    { label: "低集中", value: "低集中" },
    { label: "完全分散", value: "完全分散" },
  ];

  const BARRIER_OPTIONS = [
    { label: "高壁垒", value: "高壁垒" },
    { label: "中等壁垒", value: "中等壁垒" },
    { label: "低壁垒", value: "低壁垒" },
    { label: "无壁垒", value: "无壁垒" },
  ];

  const INDUSTRY_CATEGORY_OPTIONS = [
    { label: "科技", value: "科技" },
    { label: "金融", value: "金融" },
    { label: "能源", value: "能源" },
    { label: "医疗健康", value: "医疗健康" },
    { label: "消费", value: "消费" },
    { label: "工业", value: "工业" },
    { label: "房地产", value: "房地产" },
    { label: "通信", value: "通信" },
    { label: "交通运输", value: "交通运输" },
    { label: "公用事业", value: "公用事业" },
    { label: "其他", value: "其他" },
  ];

  const getLabel = (val: any, options: Array<{ label: string; value: any }>) => {
    if (val === null || val === undefined) return null;
    const byValue = options.find((o) => o.value === val);
    if (byValue) return byValue.label;
    const byLabel = options.find((o) => o.label === val);
    if (byLabel) return byLabel.label;
    return val;
  };

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetchCompany(id)
      .then((c) => {
        setCompany(c);
        // Normalize values for form selects: API may return either enum name or label.
        const normalized = { ...c } as any;
        if (normalized.industry_profile) {
          const ip = { ...normalized.industry_profile } as any;
          // helper: if backend returned the label (e.g. "高度集中"), convert to enum name for Select value
          const findByLabel = (val: any, options: any[]) => {
            if (!val) return val;
            const byValue = options.find((o) => o.value === val);
            if (byValue) return val;
            const byLabel = options.find((o) => o.label === val);
            if (byLabel) return byLabel.value;
            return val;
          };

          ip.concentration_level = findByLabel(ip.concentration_level, CONCENTRATION_OPTIONS);
          ip.industry_barrier = findByLabel(ip.industry_barrier, BARRIER_OPTIONS);
          ip.industry_category = findByLabel(ip.industry_category, INDUSTRY_CATEGORY_OPTIONS);
          normalized.industry_profile = ip;
        }

        form.setFieldsValue(normalized);
      })
  .catch((e) => notify.error(e, "加载失败"))
      .finally(() => setLoading(false));
  }, [id]);

  const onFinish = async (values: Company) => {
    try {
      console.log(values);
      const updated = await updateCompany(id, values);
      notify.success("保存成功");
      setEditing(false);
      router.replace(`/companies/${id}`);
    } catch (e: any) {
      notify.error(e, "保存失败");
    }
  };

  if (!company) return <main style={{ padding: 24 }}>加载中...</main>;

  return (
    <main style={{ padding: 24 }}>
      <Card title={company.name} loading={loading}>
        <Descriptions column={1} bordered>
          <Descriptions.Item label="ID">{company.id}</Descriptions.Item>
          <Descriptions.Item label="代码">{company.ticker || '-'}</Descriptions.Item>
          <Descriptions.Item label="主营业务">{company.main_business || '-'}</Descriptions.Item>
          <Descriptions.Item label="员工数">{company.employee_count || '-'}</Descriptions.Item>
          <Descriptions.Item label="行业分类">{company.industry_profile?.industry_category || '-'}</Descriptions.Item>
          <Descriptions.Item label="行业规模">{company.industry_profile?.industry_size ?? '-'}</Descriptions.Item>
          <Descriptions.Item label="集中度">{getLabel(company.industry_profile?.concentration_level, CONCENTRATION_OPTIONS) || '-'}</Descriptions.Item>
          <Descriptions.Item label="行业壁垒">{getLabel(company.industry_profile?.industry_barrier, BARRIER_OPTIONS) || '-'}</Descriptions.Item>
          <Descriptions.Item label="行业 5 年 CAGR">{company.industry_profile?.industry_cagr_5y ?? '-'}</Descriptions.Item>
          <Descriptions.Item label="主要竞争者">{company.industry_profile?.major_competitors || '-'}</Descriptions.Item>
          <Descriptions.Item label="行业趋势">{company.industry_profile?.industry_trend || '-'}</Descriptions.Item>
        </Descriptions>

      <section style={{ marginTop: 16 }}>
              {!editing ? (
                <ActionBar>
                  <Space>
                    <Button type="primary" onClick={() => setEditing(true)}>编辑</Button>
                    <Button onClick={() => router.push('/companies')}>返回</Button>
                  </Space>
                </ActionBar>
              ) : (
                <Form form={form} layout="vertical" onFinish={onFinish} initialValues={company}>
                  <Form.Item name="name" label="公司名称" rules={[{ required: true }]}> 
                    <Input />
                  </Form.Item>
                  <Form.Item name="ticker" label="代码">
                    <Input />
                  </Form.Item>
                  <Form.Item name="main_business" label="主营业务">
                    <Input />
                  </Form.Item>
                  <Form.Item name="employee_count" label="员工数">
                    <InputNumber style={{ width: '100%' }} />
                  </Form.Item>

                  {/* nested industry_profile fields */}
                  <fieldset style={{ border: '1px solid #f0f0f0', padding: 12, marginTop: 12 }}>
                    <legend style={{ padding: '0 8px' }}>行业信息</legend>
                    <Form.Item name={["industry_profile", "industry_category"]} label="行业分类">
              <Select options={INDUSTRY_CATEGORY_OPTIONS} allowClear placeholder="请选择行业分类" />
                    </Form.Item>
                    <Form.Item name={["industry_profile", "industry_size"]} label="行业规模">
                      <InputNumber style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name={["industry_profile", "concentration_level"]} label="集中度">
                      <Select options={CONCENTRATION_OPTIONS} allowClear placeholder="请选择集中度" />
                    </Form.Item>
                    <Form.Item name={["industry_profile", "industry_barrier"]} label="行业壁垒">
                      <Select options={BARRIER_OPTIONS} allowClear placeholder="请选择行业壁垒" />
                    </Form.Item>
                    <Form.Item name={["industry_profile", "industry_cagr_5y"]} label="行业 5 年 CAGR">
                      <InputNumber style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name={["industry_profile", "major_competitors"]} label="主要竞争者">
                      <Input />
                    </Form.Item>
                    <Form.Item name={["industry_profile", "industry_trend"]} label="行业趋势">
                      <Input />
                    </Form.Item>
                  </fieldset>

                  <Form.Item>
                    <Space style={{ display: 'flex', justifyContent: 'flex-end' }}>
                      <Button onClick={() => setEditing(false)}>取消</Button>
                      <Button type="primary" htmlType="submit">保存</Button>
                    </Space>
                  </Form.Item>
                </Form>
              )}
      </section>
      </Card>
    </main>
  );
}

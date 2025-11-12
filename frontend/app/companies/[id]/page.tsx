"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, Descriptions, Form, Input, InputNumber, Button, Space } from "antd";
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

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetchCompany(id)
      .then((c) => {
        setCompany(c);
        form.setFieldsValue(c);
      })
  .catch((e) => notify.error(e, "加载失败"))
      .finally(() => setLoading(false));
  }, [id]);

  const onFinish = async (values: any) => {
    try {
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
          <Descriptions.Item label="员工数">{company.employee_count ?? '-'}</Descriptions.Item>
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

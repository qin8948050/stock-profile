"use client";

import React, { useEffect, useState } from "react";
import { Table, Button, Modal, Form, Input, InputNumber, Space, Popconfirm, message } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import Link from "next/link";
import { fetchCompanies, createCompany, deleteCompany } from "../../lib/api";
import { createCompanyWithMsg, deleteCompanyWithMsg } from "../../lib/companyApi";
import notify from "../../utils/notify";
import ActionBar from "../../components/ActionBar";
import type { Company } from "../../types/company";

export default function CompaniesPage() {
  const [data, setData] = useState<Company[]>([]);
  const [loading, setLoading] = useState(false);
  const [createVisible, setCreateVisible] = useState(false);
  const [form] = Form.useForm();

  const load = async () => {
    setLoading(true);
    try {
      const list = await fetchCompanies();
      setData(list);
    } catch (err: any) {
      notify.error(err, "加载公司列表失败");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const onCreate = async (values: any) => {
    console.log("onFinish called", values);
    // also inspect current form state
    try {
      console.log("form.getFieldsValue() ->", form.getFieldsValue());
    } catch (e) {
      console.error("getFieldsValue error", e);
    }
    try {
      const res = await createCompanyWithMsg(values);
      if (res?.status === 200) {
        notify.success(res.msg || "创建成功");
        setCreateVisible(false);
        form.resetFields();
        load();
      } else {
        notify.error(res?.msg || "创建失败");
      }
    } catch (err: any) {
      notify.error(err, "创建失败");
    }
  };

  // Normal AntD onFinish handler will be used for submission

  const onDelete = async (id: number) => {
    try {
      const res = await deleteCompanyWithMsg(id);
      if (res?.status === 200) {
        notify.success(res.msg || "删除成功");
        load();
      } else {
        notify.error(res?.msg || "删除失败");
      }
    } catch (err: any) {
      notify.error(err, "删除失败");
    }
  };

  const columns = [
    { title: "ID", dataIndex: "id", key: "id" },
    { title: "公司名称", dataIndex: "name", key: "name", render: (text: any, record: Company) => <Link href={`/companies/${record.id}`}>{text}</Link> },
    { title: "代码", dataIndex: "ticker", key: "ticker" },
    { title: "主营业务", dataIndex: "main_business", key: "main_business" },
    { title: "员工数", dataIndex: "employee_count", key: "employee_count" },
    {
      title: "操作",
      key: "actions",
      render: (_: any, record: Company) => (
        <Space>
          <Link href={`/companies/${record.id}`}>查看</Link>
          <Popconfirm title="确认删除该公司吗？" onConfirm={() => onDelete(record.id)}>
            <a style={{ color: "red" }}>删除</a>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <section style={{ padding: 24 }}>
      <ActionBar>
        <Space>
          <Button onClick={() => load()}>刷新</Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setCreateVisible(true)}>新建公司</Button>
        </Space>
      </ActionBar>

      <Table rowKey={(r: any) => r.id} columns={columns} dataSource={data} loading={loading} />

      <Modal title="新建公司" open={createVisible} onCancel={() => setCreateVisible(false)} footer={null} destroyOnClose={false}>
        <Form
          form={form}
          layout="vertical"
          onFinish={onCreate}
        >
          <Form.Item name="name" label="公司名称" rules={[{ required: true, message: "请输入公司名称" }]}>
            <Input />
          </Form.Item>
          <Form.Item name="ticker" label="代码">
            <Input />
          </Form.Item>
          <Form.Item name="main_business" label="主营业务">
            <Input />
          </Form.Item>
          <Form.Item name="employee_count" label="员工数">
            <InputNumber style={{ width: "100%" }} />
          </Form.Item>
          <Form.Item>
            <Space style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button onClick={() => setCreateVisible(false)}>取消</Button>
              <Button type="primary" htmlType="submit">创建</Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </section>
  );
}

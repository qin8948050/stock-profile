"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Spin, TabsProps } from "antd";
import CardWithTabs from "../../../components/CardWithTabs";
import ProfileTab from "./ProfileTab";
import FinancialTab from "./FinancialTab"; // Import the new FinancialTab
import { fetchCompany } from "../../../lib/api";
import BusinessTab from "@/app/companies/[id]/BusinessTab";

export default function CompanyDetailPage() {
  const params = useParams();
  const id = Number(params?.id || 0);
  const [companyName, setCompanyName] = useState<string | undefined>();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
        // eslint-disable-next-line react-hooks/set-state-in-effect
      setLoading(true);
      fetchCompany(id)
        .then((c) => setCompanyName(c.name))
        .catch(() => setCompanyName("公司详情"))
        .finally(() => setLoading(false));
    }
  }, [id]);

  // Define tab items here in the page component
  const items: TabsProps["items"] = [
    {
      key: "profile",
      label: "公司资料",
      children: <ProfileTab companyId={id} />,
    },
    {
      key: "financials",
      label: "财务",
      children: <FinancialTab companyId={id} />, // Use the new FinancialTab component
    },
    // Add more tabs here in the future
      {
          key: "business",
          label:"商业分析",
          children: <BusinessTab companyId={id} />
      }
  ];

  if (loading) {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        <Spin size="large" />
      </div>
    );
  }

  return <CardWithTabs title={companyName} items={items} defaultActiveKey="profile" />;
}
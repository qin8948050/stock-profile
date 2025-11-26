"use client";

import React from "react";
import { Card, Tabs } from "antd";
import type { TabsProps } from "antd";

interface CardWithTabsProps {
  title?: string;
  items: TabsProps["items"];
  defaultActiveKey: string;
}

const CardWithTabs: React.FC<CardWithTabsProps> = ({
  title,
  items,
  defaultActiveKey,
}) => {
  return (
    <Card title={title}>
      <Tabs defaultActiveKey={defaultActiveKey} items={items} />
    </Card>
  );
};

export default CardWithTabs;
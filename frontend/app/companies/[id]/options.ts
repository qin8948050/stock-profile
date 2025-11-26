import type { Company } from "../../../types/company";

type Option = {
  label: string;
  value: string;
};

export const INDUSTRY_CATEGORY_OPTIONS: Option[] = [
  { label: "科技", value: "technology" },
  { label: "金融", value: "finance" },
  { label: "医疗保健", value: "healthcare" },
  { label: "消费品", value: "consumer_goods" },
  { label: "工业", value: "industrials" },
  { label: "能源", value: "energy" },
  { label: "房地产", value: "real_estate" },
  { label: "公用事业", value: "utilities" },
];

export const CONCENTRATION_OPTIONS: Option[] = [
  { label: "高", value: "high" },
  { label: "中", value: "medium" },
  { label: "低", value: "low" },
];

export const BARRIER_OPTIONS: Option[] = [
  { label: "高", value: "high" },
  { label: "中", value: "medium" },
  { label: "低", value: "low" },
];

/**
 * 根据 value 从 options 数组中查找对应的 label
 * @param value - 要查找的值
 * @param options - 选项数组
 * @returns 找到的 label，否则返回 value 本身
 */
export const getLabel = (
  value: string | null | undefined,
  options: Option[]
): string | null | undefined => {
  if (!value) return value;
  return options.find((opt) => opt.value === value)?.label || value;
};

/**
 * 规范化公司数据，确保 industry_profile 不为 null，以便表单绑定
 * @param company - 原始公司数据
 * @returns 规范化后的公司数据
 */
export const normalizeCompanyForForm = (company: Company): Company => {
  return {
    ...company,
    industry_profile: company.industry_profile || {},
  };
};
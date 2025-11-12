export type IndustryProfile = {
  id?: number;
  industry_category?: string | null;
  industry_size?: number | null;
  concentration_level?: string | null;
  industry_barrier?: string | null;
  industry_cagr_5y?: number | null;
  major_competitors?: string | null;
  industry_trend?: string | null;
};

export type Company = {
  id: number;
  name: string;
  ticker?: string | null;
  main_business?: string | null;
  employee_count?: number | null;
  market_position?: string | null;
  differentiation?: string | null;
  supply_chain_control?: string | null;
  industry_profile?: IndustryProfile | null;
};

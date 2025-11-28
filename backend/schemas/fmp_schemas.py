from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from pydantic.alias_generators import to_camel

class FMPBalanceSheetSchema(BaseModel):
    """
    Represents the structure of a balance sheet item from the FMP API.
    It automatically converts camelCase from the API to snake_case in Python.
    """
    # 使用 Field 和 alias 来处理大小写不一致的特殊情况
    cash_and_short_term_investments: Optional[int] = Field(alias="cashAndShortTermInvestments")

    # 其他所有字段将自动从 camelCase 转换为 snake_case
    date: str
    symbol: str
    cik: Optional[str] = None
    filing_date: Optional[str] = Field(alias="filingDate")
    fiscal_year: str = Field(alias="fiscalYear")
    period: str
    cash_and_cash_equivalents: Optional[int] = None
    short_term_investments: Optional[int] = None
    net_receivables: Optional[int] = None
    other_current_assets: Optional[int] = None
    total_current_assets: Optional[int] = None
    property_plant_equipment_net: Optional[int] = None
    long_term_investments: Optional[int] = None
    other_non_current_assets: Optional[int] = None
    total_non_current_assets: Optional[int] = None
    total_assets: Optional[int] = None
    total_current_liabilities: Optional[int] = None
    short_term_debt: Optional[int] = None
    account_payables: Optional[int] = None
    other_current_liabilities: Optional[int] = None
    long_term_debt: Optional[int] = None
    other_non_current_liabilities: Optional[int] = None
    total_non_current_liabilities: Optional[int] = None
    total_liabilities: Optional[int] = None
    common_stock: Optional[int] = None
    retained_earnings: Optional[int] = None
    accumulated_other_comprehensive_income_loss: Optional[int] = None
    total_stockholders_equity: Optional[int] = None
    total_liabilities_and_total_equity: Optional[int] = None

    model_config = ConfigDict(
        alias_generator=to_camel, # 全局别名生成器
        populate_by_name=True,    # 允许按字段名（snake_case）和别名（camelCase）填充
        from_attributes=True,
        extra='allow'             # 允许 JSON 中有多余的字段
    )

class FMPIncomeStatementSchema(BaseModel):
    """
    Represents the structure of an income statement item from the FMP API.
    It automatically converts camelCase from the API to snake_case in Python.
    """
    date: str
    symbol: str
    cik: Optional[str] = None
    filing_date: Optional[str] = Field(alias="filingDate")
    fiscal_year: str = Field(alias="fiscalYear")
    period: str
    revenue: Optional[int] = None
    cost_of_revenue: Optional[int] = None
    gross_profit: Optional[int] = None
    research_and_development_expenses: Optional[int] = None
    general_and_administrative_expenses: Optional[int] = None
    selling_and_marketing_expenses: Optional[int] = None
    selling_general_and_administrative_expenses: Optional[int] = None
    other_expenses: Optional[int] = None
    operating_expenses: Optional[int] = None
    cost_and_expenses: Optional[int] = None
    net_interest_income: Optional[int] = None
    interest_income: Optional[int] = None
    interest_expense: Optional[int] = None
    depreciation_and_amortization: Optional[int] = None
    ebitda: Optional[int] = None
    ebit: Optional[int] = None
    non_operating_income_excluding_interest: Optional[int] = None
    operating_income: Optional[int] = None
    total_other_income_expenses_net: Optional[int] = None
    income_before_tax: Optional[int] = None
    income_tax_expense: Optional[int] = None
    net_income_from_continuing_operations: Optional[int] = None
    net_income_from_discontinued_operations: Optional[int] = None
    other_adjustments_to_net_income: Optional[int] = None
    net_income: Optional[int] = None
    net_income_deductions: Optional[int] = None
    bottom_line_net_income: Optional[int] = None
    eps: Optional[float] = None
    eps_diluted: Optional[float] = None
    weighted_average_shs_out: Optional[int] = None
    weighted_average_shs_out_dil: Optional[int] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        extra='allow'
    )

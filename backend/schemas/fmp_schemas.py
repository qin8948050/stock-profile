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
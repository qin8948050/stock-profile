from sqlalchemy import Column, String, Integer, Date, BigInteger, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

from models import Base, TimestampMixin
from models.base import FinancialBaseMixin


class CashSheetStatementCore(Base, FinancialBaseMixin, TimestampMixin):
    __tablename__ = 'cash_sheet_statement_core'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")

    net_income = Column(BigInteger, nullable=True, comment="Net Income")
    depreciation_and_amortization = Column(BigInteger, nullable=True, comment="Depreciation and Amortization")
    deferred_income_tax = Column(BigInteger, nullable=True, comment="Deferred Income Tax")
    stock_based_compensation = Column(BigInteger, nullable=True, comment="Stock Based Compensation")
    change_in_working_capital = Column(BigInteger, nullable=True, comment="Change in Working Capital")
    accounts_receivables = Column(BigInteger, nullable=True, comment="Accounts Receivables")
    inventory = Column(BigInteger, nullable=True, comment="Inventory")
    accounts_payables = Column(BigInteger, nullable=True, comment="Accounts Payables")
    other_working_capital = Column(BigInteger, nullable=True, comment="Other Working Capital")
    other_non_cash_items = Column(BigInteger, nullable=True, comment="Other Non-cash Items")
    net_cash_provided_by_operating_activities = Column(BigInteger, nullable=True, comment="Net Cash Provided by Operating Activities")
    investments_in_property_plant_and_equipment = Column(BigInteger, nullable=True, comment="Investments in Property, Plant and Equipment")
    acquisitions_net = Column(BigInteger, nullable=True, comment="Acquisitions Net")
    purchases_of_investments = Column(BigInteger, nullable=True, comment="Purchases of Investments")
    sales_maturities_of_investments = Column(BigInteger, nullable=True, comment="Sales/Maturities of Investments")
    other_investing_activites = Column(BigInteger, nullable=True, comment="Other Investing Activites")
    net_cash_used_for_investing_activites = Column(BigInteger, nullable=True, comment="Net Cash Used for Investing Activites")
    debt_repayment = Column(BigInteger, nullable=True, comment="Debt Repayment")
    common_stock_issued = Column(BigInteger, nullable=True, comment="Common Stock Issued")
    common_stock_repurchased = Column(BigInteger, nullable=True, comment="Common Stock Repurchased")
    dividends_paid = Column(BigInteger, nullable=True, comment="Dividends Paid")
    other_financing_activites = Column(BigInteger, nullable=True, comment="Other Financing Activites")
    net_cash_used_provided_by_financing_activities = Column(BigInteger, nullable=True, comment="Net Cash Used/Provided by Financing Activities")
    effect_of_forex_changes_on_cash = Column(BigInteger, nullable=True, comment="Effect of Forex Changes on Cash")
    net_change_in_cash = Column(BigInteger, nullable=True, comment="Net Change in Cash")
    cash_at_end_of_period = Column(BigInteger, nullable=True, comment="Cash at End of Period")
    cash_at_beginning_of_period = Column(BigInteger, nullable=True, comment="Cash at Beginning of Period")
    operating_cash_flow = Column(BigInteger, nullable=True, comment="Operating Cash Flow")
    capital_expenditure = Column(BigInteger, nullable=True, comment="Capital Expenditure")
    free_cash_flow = Column(BigInteger, nullable=True, comment="Free Cash Flow")

    # 关系：关联回 Company
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship('Company', back_populates='cash_sheets')
    # 关系：一对多关联到 EAV 属性
    eav_attributes = relationship('CashSheetStatementEAV', back_populates='statement', cascade="all, delete-orphan")


class CashSheetStatementEAV(Base, TimestampMixin):
    __tablename__ = 'cash_sheet_statement_eav'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    cash_statement_id = Column(Integer, ForeignKey('cash_sheet_statement_core.id'), nullable=False, index=True, comment="报表ID")
    attribute_name = Column(String(100), nullable=False, comment="属性名")

    # 稀疏列：根据值的类型，只填充其中一列
    value_string = Column(Text, nullable=True, comment="字符串类型的值")
    value_numeric = Column(BigInteger, nullable=True, comment="数字类型的值")

    # 关系：关联回报表核心
    statement = relationship('CashSheetStatementCore', back_populates='eav_attributes')

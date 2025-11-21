from sqlalchemy import Column, String, Integer, Date, BigInteger, ForeignKey, Text
from sqlalchemy.orm import relationship

from models import Base, TimestampMixin

class FinancialBaseMixin:

    # ---------- Meta Info ----------
    symbol = Column(String(20), index=True, nullable=False, comment="Ticker symbol")
    cik = Column(String(20), nullable=True, comment="CIK number")

    date = Column(Date, nullable=False, comment="Statement date")
    filing_date = Column(Date, nullable=True, comment="Filing date")

    fiscal_year = Column(String(10), nullable=False, comment="Fiscal year")
    period = Column(String(10), nullable=False, comment="Reporting period (FY/Q1/Q2/Q3)")

class BalanceSheetStatementCore(Base, FinancialBaseMixin,TimestampMixin):
    __tablename__ = 'balance_sheet_statement_core'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    # ---------- Assets ----------
    cash_and_cash_equivalents = Column(BigInteger, nullable=True, comment="Cash and cash equivalents")
    short_term_investments = Column(BigInteger, nullable=True, comment="Short-term investments")
    cash_and_short_term_investments = Column(BigInteger, nullable=True, comment="Cash and short-term investments")

    net_receivables = Column(BigInteger, nullable=True, comment="Net receivables")
    other_current_assets = Column(BigInteger, nullable=True, comment="Other current assets")
    total_current_assets = Column(BigInteger, nullable=True, comment="Total current assets")

    property_plant_equipment_net = Column(BigInteger, nullable=True, comment="Net property, plant and equipment")
    long_term_investments = Column(BigInteger, nullable=True, comment="Long-term investments")
    other_non_current_assets = Column(BigInteger, nullable=True, comment="Other non-current assets")
    total_non_current_assets = Column(BigInteger, nullable=True, comment="Total non-current assets")

    total_assets = Column(BigInteger, nullable=False, comment="Total assets")

    # ---------- Liabilities ----------
    total_current_liabilities = Column(BigInteger, nullable=True, comment="Total current liabilities")
    short_term_debt = Column(BigInteger, nullable=True, comment="Short-term debt")
    account_payables = Column(BigInteger, nullable=True, comment="Accounts payable")
    other_current_liabilities = Column(BigInteger, nullable=True, comment="Other current liabilities")

    long_term_debt = Column(BigInteger, nullable=True, comment="Long-term debt")
    other_non_current_liabilities = Column(BigInteger, nullable=True, comment="Other non-current liabilities")
    total_non_current_liabilities = Column(BigInteger, nullable=True, comment="Total non-current liabilities")

    total_liabilities = Column(BigInteger, nullable=False, comment="Total liabilities")

    # ---------- Stockholders' Equity ----------
    common_stock = Column(BigInteger, nullable=True, comment="Common stock")
    retained_earnings = Column(BigInteger, nullable=True, comment="Retained earnings")
    accumulated_other_comprehensive_income_loss = Column(
        BigInteger, nullable=True,
        comment="Accumulated other comprehensive income/loss"
    )

    total_stockholders_equity = Column(BigInteger, nullable=True, comment="Total stockholders' equity")
    total_liabilities_and_total_equity = Column(BigInteger, nullable=True, comment="Liabilities and equity total")

    # 关系：关联回 Company
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship('Company', back_populates='balance_sheets')
    # 关系：一对多关联到 EAV 属性
    eav_attributes = relationship('BalanceSheetStatementEAV', back_populates='statement', cascade="all, delete-orphan")


class BalanceSheetStatementEAV(Base, TimestampMixin):
    __tablename__ = 'balance_sheet_statement_eav'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    balance_statement_id = Column(Integer, ForeignKey('balance_sheet_statement_core.id'), nullable=False, index=True, comment="报表ID")
    attribute_name = Column(String(100), nullable=False, comment="属性名, e.g., '存货', '商誉'")

    # 稀疏列：根据值的类型，只填充其中一列
    value_string = Column(Text, nullable=True, comment="字符串类型的值")
    value_numeric = Column(BigInteger, nullable=True, comment="数字类型的值")

    # 关系：关联回报表核心
    statement = relationship('BalanceSheetStatementCore', back_populates='eav_attributes')
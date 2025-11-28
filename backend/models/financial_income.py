from sqlalchemy import Column, String, Integer, Date, BigInteger, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

from models import Base, TimestampMixin
from models.base import FinancialBaseMixin


class IncomeSheetStatementCore(Base, FinancialBaseMixin, TimestampMixin):
    __tablename__ = 'income_sheet_statement_core'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")

    revenue = Column(BigInteger, nullable=True, comment="Revenue")
    cost_of_revenue = Column(BigInteger, nullable=True, comment="Cost of revenue")
    gross_profit = Column(BigInteger, nullable=True, comment="Gross profit")
    research_and_development_expenses = Column(BigInteger, nullable=True, comment="Research and development expenses")
    general_and_administrative_expenses = Column(BigInteger, nullable=True, comment="General and administrative expenses")
    selling_and_marketing_expenses = Column(BigInteger, nullable=True, comment="Selling and marketing expenses")
    selling_general_and_administrative_expenses = Column(BigInteger, nullable=True, comment="Selling, general and administrative expenses")
    other_expenses = Column(BigInteger, nullable=True, comment="Other expenses")
    operating_expenses = Column(BigInteger, nullable=True, comment="Operating expenses")
    cost_and_expenses = Column(BigInteger, nullable=True, comment="Cost and expenses")
    net_interest_income = Column(BigInteger, nullable=True, comment="Net interest income")
    interest_income = Column(BigInteger, nullable=True, comment="Interest income")
    interest_expense = Column(BigInteger, nullable=True, comment="Interest expense")
    depreciation_and_amortization = Column(BigInteger, nullable=True, comment="Depreciation and amortization")
    ebitda = Column(BigInteger, nullable=True, comment="EBITDA")
    ebit = Column(BigInteger, nullable=True, comment="EBIT")
    non_operating_income_excluding_interest = Column(BigInteger, nullable=True, comment="Non-operating income excluding interest")
    operating_income = Column(BigInteger, nullable=True, comment="Operating income")
    total_other_income_expenses_net = Column(BigInteger, nullable=True, comment="Total other income/expenses net")
    income_before_tax = Column(BigInteger, nullable=True, comment="Income before tax")
    income_tax_expense = Column(BigInteger, nullable=True, comment="Income tax expense")
    net_income_from_continuing_operations = Column(BigInteger, nullable=True, comment="Net income from continuing operations")
    net_income_from_discontinued_operations = Column(BigInteger, nullable=True, comment="Net income from discontinued operations")
    other_adjustments_to_net_income = Column(BigInteger, nullable=True, comment="Other adjustments to net income")
    net_income = Column(BigInteger, nullable=True, comment="Net income")
    net_income_deductions = Column(BigInteger, nullable=True, comment="Net income deductions")
    bottom_line_net_income = Column(BigInteger, nullable=True, comment="Bottom line net income")
    eps = Column(Float, nullable=True, comment="EPS")
    eps_diluted = Column(Float, nullable=True, comment="EPS diluted")
    weighted_average_shs_out = Column(BigInteger, nullable=True, comment="Weighted average shares outstanding")
    weighted_average_shs_out_dil = Column(BigInteger, nullable=True, comment="Weighted average shares outstanding diluted")

    # 关系：关联回 Company
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship('Company', back_populates='income_sheets')
    # 关系：一对多关联到 EAV 属性
    eav_attributes = relationship('IncomeSheetStatementEAV', back_populates='statement', cascade="all, delete-orphan")


class IncomeSheetStatementEAV(Base, TimestampMixin):
    __tablename__ = 'income_sheet_statement_eav'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    income_statement_id = Column(Integer, ForeignKey('income_sheet_statement_core.id'), nullable=False, index=True, comment="报表ID")
    attribute_name = Column(String(100), nullable=False, comment="属性名")

    # 稀疏列：根据值的类型，只填充其中一列
    value_string = Column(Text, nullable=True, comment="字符串类型的值")
    value_numeric = Column(BigInteger, nullable=True, comment="数字类型的值")

    # 关系：关联回报表核心
    statement = relationship('IncomeSheetStatementCore', back_populates='eav_attributes')

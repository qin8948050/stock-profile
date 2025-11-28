from datetime import datetime, timezone, timedelta

from sqlalchemy import Column, DateTime, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# 定义东八区时区对象
CST = timezone(timedelta(hours=8))

def now_cst():
    """返回当前东八区时间"""
    return datetime.now(CST)

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=now_cst)
    updated_at = Column(DateTime(timezone=True), default=now_cst, onupdate=now_cst)


class FinancialBaseMixin:

    # ---------- Meta Info ----------
    symbol = Column(String(20), index=True, nullable=False, comment="Ticker symbol")
    cik = Column(String(20), nullable=True, comment="CIK number")

    date = Column(Date, nullable=False, comment="Statement date")
    filing_date = Column(Date, nullable=True, comment="Filing date")

    fiscal_year = Column(String(10), nullable=False, comment="Fiscal year")
    period = Column(String(10), nullable=False, comment="Reporting period (FY/Q1/Q2/Q3)")
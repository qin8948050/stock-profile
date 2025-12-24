from sqlalchemy import Column, Integer, String, Float, ForeignKey, TEXT, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, TimestampMixin

class CompanyMetric(Base, TimestampMixin):
    __tablename__ = "company_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True, comment="公司ID")
    
    # 核心抽象字段
    metric_code = Column(String(50), index=True)  # 指标代号，如 "PEG", "DCF_5Y"
    
    value = Column(Float)                     # 计算结果
    
    # 存储计算时的输入参数
    input_params = Column(TEXT, nullable=True)

    # 新增字段
    valuation_date = Column(DateTime, default=datetime.utcnow, index=True, comment="估值基准日期(通常是股价日期)")
    period = Column(String(20), nullable=True, comment="财报周期(如 2023-Q3)")

    company = relationship(
        "Company",
        back_populates="company_metrics",
    )

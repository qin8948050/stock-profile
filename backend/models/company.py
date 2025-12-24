from enum import Enum

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SqlEnum, Float
from sqlalchemy.orm import relationship

from models.base import Base,TimestampMixin


class IndustryCategoryEnum(str, Enum):
    TECHNOLOGY = "科技"
    FINANCE = "金融"
    ENERGY = "能源"
    HEALTHCARE = "医疗健康"
    CONSUMER = "消费"
    INDUSTRIAL = "工业"
    REAL_ESTATE = "房地产"
    TELECOM = "通信"
    TRANSPORT = "交通运输"
    UTILITIES = "公用事业"
    OTHER = "其他"


class IndustryConcentrationEnum(str, Enum):
    """
    CR4（前4大企业市场份额）≥ 70%:高度集中，40% ~ 70%：中等集中，20% ~ 40%：低等集中，< 20%：完全分散
    """
    HIGH = "高度集中"
    MEDIUM = "中等集中"
    LOW = "低集中"
    VERY_LOW = "完全分散"

#TODO:自动评估
class IndustryBarrierEnum(str, Enum):
    """
    | 维度          | 高壁垒              | 中壁垒           | 低壁垒          | 说明                 |
    | ----------- | ---------------- | ------------- | ------------ | ------------------ |
    | **资金门槛**    | 投入巨大 (>数十亿/行业)   | 投入适中          | 投入小，门槛低      | 包括固定资产、研发投入、启动资金   |
    | **技术/研发**   | 核心技术复杂、专利多、研发周期长 | 技术需要一定能力，易被模仿 | 技术易获取，标准化    | 技术门槛越高，壁垒越高        |
    | **品牌/客户黏性** | 龙头品牌高度认可，客户忠诚度高  | 品牌有一定影响力      | 品牌影响力小或客户易流动 | 品牌壁垒可量化为市场调研/客户留存率 |
    | **渠道/供应链**  | 关键渠道掌握在少数企业手中    | 渠道可进入但有成本     | 渠道开放，进入容易    | 渠道壁垒包括分销、物流、合作伙伴网络 |
    | **政策/法规**   | 强监管、许可证/准入限制     | 有部分规范，合规成本可控  | 无特别限制        | 适用于银行、医药、能源等行业     |

    """
    HIGH = "高壁垒"
    MEDIUM = "中等壁垒"
    LOW = "低壁垒"
    NONE = "无壁垒"

class MarketPositionEnum(str, Enum):
    """市场地位"""
    LEADER = "全球领先 – 在高端消费电子/智能硬件市场居前列"
    UPPER_MIDDLE = "中上水平 – 在整体硬件数量市场份额中居中"
    CHALLENGER = "追赶型 – 市场份额有限，但增长迅速"
    WEAK = "弱势 – 市场份额低，竞争压力大"

class SupplyChainControlEnum(str, Enum):
    """供应链控制力"""
    STRONG = "强"
    MEDIUM = "中等"
    WEAK = "弱"

class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True, comment="公司名称")
    ticker = Column(String(50), nullable=True, unique=True, comment="股票代码")
    main_business = Column(String(100), nullable=True, comment="主营业务")
    employee_count = Column(Integer, nullable=True, comment="员工数量")
    market_position = Column(SqlEnum(MarketPositionEnum), nullable=True, comment="市场地位")
    differentiation = Column(Text, nullable=True, comment="产品/服务差异化特点")
    supply_chain_control = Column(SqlEnum(SupplyChainControlEnum), nullable=True, comment="供应链控制力")
    # 一对一关联
    industry_profile = relationship("IndustryProfile", back_populates="company", uselist=False, cascade="all, delete-orphan")
    # competitiveness_profile = relationship("CompetitivenessProfile", back_populates="company", uselist=False, cascade="all, delete-orphan")

    # 一对多关联: 一个公司可以有多张财务报表
    balance_sheets = relationship("BalanceSheetStatementCore", back_populates="company", cascade="all, delete-orphan")
    income_sheets = relationship("IncomeSheetStatementCore", back_populates="company", cascade="all, delete-orphan")
    cash_sheets = relationship("CashSheetStatementCore", back_populates="company", cascade="all, delete-orphan")
    company_metrics = relationship("CompanyMetric", back_populates="company", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Company(name={self.name}, ticker={self.ticker})>"


class IndustryProfile(Base, TimestampMixin):
    __tablename__ = "industry_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, unique=True, index=True, comment="公司ID")
    industry_category = Column(SqlEnum(IndustryCategoryEnum), nullable=True, comment="行业分类")
    industry_size = Column(Float, nullable=True, comment="行业规模或市场容量(亿美元)，总销售额法")
    concentration_level = Column(SqlEnum(IndustryConcentrationEnum), nullable=True, comment="行业集中度")
    industry_barrier = Column(SqlEnum(IndustryBarrierEnum), nullable=True, comment="行业壁垒（高/中/低/无")
    industry_cagr_5y = Column(Float, nullable=True, comment="5年复合增速（%）")
    major_competitors = Column(Text, nullable=True, comment="主要竞争对手")
    industry_trend = Column(Text, nullable=True, comment="行业趋势")

    company = relationship(
        "Company",
        back_populates="industry_profile",
    )

    def __repr__(self):
        return f"<IndustryProfile(id={self.id}, company_id={self.company_id}, industry_category='{self.industry_category}')>"

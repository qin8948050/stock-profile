from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List, Any
from models.company import IndustryCategoryEnum, IndustryConcentrationEnum, IndustryBarrierEnum, MarketPositionEnum, \
    SupplyChainControlEnum


# ===================================================================
# IndustryProfile Schemas
# ===================================================================

class IndustryProfileBase(BaseModel):
    """基础的行业画像 Schema，包含所有可由用户输入的字段"""
    industry_category: Optional[IndustryCategoryEnum] = None
    industry_size: Optional[float] = None
    concentration_level: Optional[IndustryConcentrationEnum] = None
    industry_barrier: Optional[IndustryBarrierEnum] = None
    industry_cagr_5y: Optional[float] = None
    major_competitors:Optional[str] = None
    industry_trend:Optional[str] = None
    #TODO: 跳过校验，只用于测试
    @field_validator('concentration_level', 'industry_barrier', mode='before')
    @classmethod
    def empty_str_to_none(cls, v: Any) -> Optional[Any]:
        """将空字符串转换为 None"""
        return None if v == "" else v


class IndustryProfileCreate(IndustryProfileBase):
    """创建行业画像时使用的 Schema"""
    pass


class IndustryProfileUpdate(IndustryProfileBase):
    """更新行业画像时使用的 Schema，所有字段都是可选的"""
    pass


class IndustryProfileInDB(IndustryProfileBase):
    """从数据库读取并返回给客户端的 Schema"""
    id: int

    model_config = ConfigDict(
        from_attributes=True  # 允许从 ORM 模型直接转换
    )


# ===================================================================
# Company Schemas
# ===================================================================

class CompanyBase(BaseModel):
    """基础的公司 Schema"""
    name: str
    ticker: Optional[str] = None
    main_business: Optional[str] = None
    employee_count: Optional[int] = None
    market_position:Optional[MarketPositionEnum] = None
    differentiation:Optional[str] = None
    supply_chain_control:Optional[SupplyChainControlEnum] = None
    #TODO: 跳过校验，只用于测试
    @field_validator('market_position', 'supply_chain_control', mode='before')
    @classmethod
    def empty_str_to_none(cls, v: Any) -> Optional[Any]:
        """将空字符串转换为 None"""
        return None if v == "" else v

class CompanyCreate(CompanyBase):
    """创建公司时使用的 Schema，嵌套了 IndustryProfileCreate"""
    industry_profile: Optional[IndustryProfileCreate] = None


class CompanyUpdate(CompanyBase):
    """更新公司时使用的 Schema，所有字段可选"""
    industry_profile: Optional[IndustryProfileUpdate] = None


class CompanyInDB(CompanyBase):
    """从数据库读取并返回给客户端的 Schema，嵌套了 IndustryProfileInDB"""
    id: int
    industry_profile: Optional[IndustryProfileInDB] = None

    model_config = ConfigDict(
        from_attributes=True  # 允许从 ORM 模型直接转换
    )
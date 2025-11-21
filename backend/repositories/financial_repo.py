from typing import Dict, List, Union, Any
from pydantic import BaseModel
from fastapi import HTTPException, status
from pandas.core.interchange.dataframe_protocol import Column
from pydantic.alias_generators import to_camel

from repositories import BaseRepository
from sqlalchemy.orm import Session
from models.financial import BalanceSheetStatementCore,BalanceSheetStatementEAV
from repositories.base import BaseRepository
from schemas.financial import FinancialStatementType
from schemas.fmp_schemas import FMPBalanceSheetSchema
from modules.data_loader.base import DataLoader
from modules.data_loader.fmp_loader import FMPBalanceSheetLoader
from core.config import config
from utils.case_converter import convert_keys_to_snake_case


def get_statement_dependencies(statement_type: FinancialStatementType) -> tuple[DataLoader, BaseRepository]:
    """
    通用工厂函数，根据报表类型返回对应的 Loader 和 Repository。
    """
    # 映射表，用于配置不同报表类型对应的依赖
    dependency_map = {
        FinancialStatementType.BALANCE: (FMPBalanceSheetLoader(config=config), BalanceStatementRepository()),
        # 以后可以轻松扩展，例如:
        # FinancialStatementType.INCOME: (FMPIncomeStatementLoader(config=config), IncomeStatementRepository()),
    }

    dependencies = dependency_map.get(statement_type)
    if dependencies is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported financial statement type: {statement_type}")

    return dependencies

class BalanceStatementRepository(BaseRepository[BalanceSheetStatementCore]):
    def __init__(self):
        super().__init__(
            BalanceSheetStatementCore,
            eav_model=BalanceSheetStatementEAV,
            eav_fk_name="balance_statement_id"
        )

    def _upsert_single(self, db: Session, *, data: Dict[str, Any], **kwargs) -> BalanceSheetStatementCore:
        """
        Upserts a single balance sheet record from a dictionary without committing.
        The company_id is expected to be passed via kwargs.
        """
        company_id = kwargs.get("company_id")

        snake_case_data = convert_keys_to_snake_case(data)
        parsed_data = FMPBalanceSheetSchema.model_validate(snake_case_data)

        # 1️⃣ 区分核心字段和 EAV 字段
        # 获取在 FMPBalanceSheetSchema 中明确定义的核心字段
        core_field_names = set(FMPBalanceSheetSchema.model_fields.keys())
        # 从验证过的数据中只提取核心字段的值
        core_data_dict = parsed_data.model_dump(include=core_field_names, exclude_unset=True)

        # 核心字段
        core_fields = {"company_id": company_id, **core_data_dict}

        # 2️⃣ 查找或创建核心表记录 (Upsert)
        # 使用 .get() 安全地访问唯一键，并提供更明确的错误处理
        symbol = core_fields.get("symbol")
        fiscal_year = core_fields.get("fiscal_year")
        period = core_fields.get("period")

        if not all([symbol, fiscal_year, period]):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Incomplete data: 'symbol', 'fiscal_year', and 'period' are required for upsert."
            )

        core_obj = db.query(self.model).filter_by(symbol=symbol, fiscal_year=fiscal_year, period=period).first()

        if core_obj:
            # 更新已存在的记录
            for key, value in core_fields.items():
                setattr(core_obj, key, value)
            # 删除旧的 EAV 记录
            db.query(BalanceSheetStatementEAV).filter_by(balance_statement_id=core_obj.id).delete()
        else:
            # 创建新记录
            core_obj = self.model(**core_fields)
            db.add(core_obj)
            # 立即刷新以获取 core_obj.id
            db.flush()

        # 3️⃣ 保存 EAV 可变字段
        # 从已验证的数据中排除核心字段，剩下的就是 EAV 字段
        eav_data = parsed_data.model_dump(exclude=core_field_names, exclude_unset=True)
        if eav_data:
            self._save_eav_attributes(db, core_obj=core_obj, data=eav_data, excluded_keys=set())

        return core_obj
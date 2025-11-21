from typing import Dict, List, Union, Any
from pydantic import BaseModel
from fastapi import HTTPException, status
from pandas.core.interchange.dataframe_protocol import Column

from repositories import BaseRepository
from sqlalchemy.orm import Session
from models.financial import BalanceSheetStatementCore,BalanceSheetStatementEAV
from repositories.base import BaseRepository
from schemas.financial import FinancialStatementType
from modules.data_loader.base import DataLoader
from modules.data_loader.fmp_loader import FMPBalanceSheetLoader
from core.config import config


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
            eav_fk_name="statement_id"
        )

    def _upsert_single(self, db: Session, *, data: Dict[str, Any], **kwargs) -> BalanceSheetStatementCore:
        """
        Upserts a single balance sheet record from a dictionary without committing.
        The company_id is expected to be passed via kwargs.
        """
        company_id = kwargs.get("company_id")
        # 核心字段
        core_fields = {
            "company_id": company_id,
            "cik":data.get("cik"),
            "symbol": data.get("symbol"),
            "date":data.get("date"),
            "filing_date":data.get("filingDate"),
            "fiscal_year": int(data.get("fiscalYear")),
            "cash_and_cash_equivalents": data.get("cashAndCashEquivalents"),
            "short_term_investments": data.get("shortTermInvestments"),
            "cash_and_short_term_investments": data.get("CashAndShortTermInvestments"),
            "net_receivables": data.get("netReceivables"),
            "other_current_assets": data.get("otherCurrentAssets"),
            "total_current_assets": data.get("totalCurrentAssets"),
            "property_plant_equipment_net": data.get("propertyPlantEquipmentNet"),
            "long_term_investments": data.get("longTermInvestments"),
            "other_non_current_assets": data.get("otherNonCurrentAssets"),
            "total_non_current_assets": data.get("totalNonCurrentAssets"),
            "total_assets": data.get("totalAssets"),
            "total_current_liabilities": data.get("totalCurrentLiabilities"),
            "short_term_debt": data.get("shortTermDebt"),
            "account_payables": data.get("accountPayables"),
            "other_current_liabilities": data.get("otherCurrentLiabilities"),
            "long_term_debt": data.get("longTermDebt"),
            "other_non_current_liabilities": data.get("otherNonCurrentLiabilities"),
            "total_non_current_liabilities": data.get("totalNonCurrentLiabilities"),
            "total_liabilities": data.get("totalLiabilities"),
            "common_stock": data.get("commonStock"),
            "retained_earnings": data.get("retainedEarnings"),
            "accumulated_other_comprehensive_income_loss": data.get("accumulatedOtherComprehensiveIncomeLoss"),
            "total_stockholders_equity": data.get("totalStockholdersEquity"),
            "total_liabilities_and_total_equity": data.get("totalLiabilitiesAndTotalEquity"),
            "period": data.get("period")
        }

        # 1️⃣ 查找或创建核心表记录 (Upsert)
        core_obj = db.query(self.model).filter_by(
            symbol=core_fields["symbol"],
            fiscal_year=core_fields["fiscal_year"],
            period=core_fields["period"]
        ).first()

        if core_obj:
            # 更新已存在的记录
            for key, value in core_fields.items():
                setattr(core_obj, key, value)
            # 删除旧的 EAV 记录
            db.query(BalanceSheetStatementEAV).filter_by(balance_sheet_id=core_obj.id).delete()
        else:
            # 创建新记录
            core_obj = self.model(**core_fields)
            db.add(core_obj)
            # 立即刷新以获取 core_obj.id
            db.flush()

        # 2️⃣ 保存 EAV 可变字段
        # 这里的 excluded_keys 仍然是特定于此仓库的，因为它知道哪些原始键被映射到了核心字段
        excluded_keys = set(core_fields.keys()) | {"date", "fiscalYear", "period"}
        self._save_eav_attributes(db, core_obj=core_obj, data=data, excluded_keys=excluded_keys)

        return core_obj
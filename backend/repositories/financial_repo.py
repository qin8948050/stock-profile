from typing import Dict

from pandas.core.interchange.dataframe_protocol import Column

from repositories import BaseRepository
from sqlalchemy.orm import Session
from models.financial import BalanceSheetStatementCore,BalanceSheetStatementEAV
from repositories.base import BaseRepository

class BalanceStatementRepository(BaseRepository[BalanceSheetStatementCore]):
    def __init__(self):
        super().__init__(BalanceSheetStatementCore)

    def upsert_from_json(self, db: Session, company_id: int, data: Dict) -> BalanceSheetStatementCore:
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
            core_obj = self.create(db, obj_in=core_fields)
            # 立即刷新以获取 core_obj.id
            db.flush()

        # 2️⃣ 保存 EAV 可变字段
        excluded_keys = set(core_fields.keys()) | {"date", "fiscalYear", "period"}
        for key, value in data.items():
            if key not in excluded_keys:
                eav_obj = BalanceSheetStatementEAV(
                    balance_sheet_id=core_obj.id,
                    metric_name=key,
                    metric_value=str(value) if value is not None else None
                )
                db.add(eav_obj)
        db.commit()
        db.refresh(core_obj)
        return core_obj
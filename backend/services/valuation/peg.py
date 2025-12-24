from sqlalchemy.orm import Session
from typing import Dict, Any
from .base_valuation import ValuationStrategy
from .constants import ValuationMetricType

class PegValuationStrategy(ValuationStrategy):
    metric_code = ValuationMetricType.PEG.value

    def calculate(self, company_id: int, inputs: Dict[str, Any], db: Session) -> float:
        # 1. 获取输入参数
        growth_rate = inputs.get("growth_rate")
        pe_ratio = inputs.get("pe_ratio")

        # 校验
        if growth_rate is None:
            raise ValueError("Growth rate is required for PEG calculation")
        
        # 如果前端没传 PE，这里可以尝试从数据库查 (这里先简化为必须传入或抛错)
        if pe_ratio is None:
            # TODO: 从 FinancialRepository 获取最新 PE
            # pe_ratio = financial_repo.get_latest_pe(db, company_id)
            raise ValueError("PE Ratio is required (or fetch from DB)")

        # 2. 执行计算
        # PEG = PE / (Growth Rate * 100) 通常 Growth Rate 是百分比，比如 15% -> 15
        # 这里假设输入就是 15
        if float(growth_rate) == 0:
            return 0.0
            
        raw_peg = float(pe_ratio) / float(growth_rate)
        
        # 3. 精确到两位小数
        return round(raw_peg, 2)

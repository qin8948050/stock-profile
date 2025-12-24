from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime

from repositories.valuation_repo import ValuationRepository
from services.valuation.peg import PegValuationStrategy
from services.valuation.base_valuation import ValuationStrategy
from services.valuation.constants import ValuationMetricType

class ValuationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ValuationRepository()
        # 注册所有策略
        self._strategies: Dict[str, ValuationStrategy] = {
            ValuationMetricType.PEG.value: PegValuationStrategy(),
            # 未来添加: ValuationMetricType.DCF.value: DcfValuationStrategy(),
        }

    def calculate_and_save(self, company_id: int, metric_code: str, inputs: Dict[str, Any]):
        # 1. 找到对应的策略
        strategy = self._strategies.get(metric_code)
        if not strategy:
            raise ValueError(f"Unknown valuation metric: {metric_code}")

        # 2. 执行计算
        result_value = strategy.calculate(company_id, inputs, self.db)
        
        # TODO: 从 inputs 或策略返回结果中提取 period 和 valuation_date
        # 目前假设 valuation_date 为当前时间，period 为空
        # 如果 inputs 里有 'period'，可以提取出来
        period = inputs.get("period")
        valuation_date = inputs.get("valuation_date") # 如果前端传了日期

        # 3. 保存结果
        metric_record = self.repo.save_metric(
            self.db, 
            company_id, 
            metric_code, 
            result_value, 
            inputs,
            period=period,
            valuation_date=valuation_date
        )
        
        return metric_record

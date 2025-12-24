from sqlalchemy.orm import Session
from models.company_metric import CompanyMetric
from typing import Dict, Any, Optional
from datetime import datetime
import json

class ValuationRepository:
    def save_metric(
        self, 
        db: Session, 
        company_id: int, 
        metric_code: str, 
        value: float, 
        inputs: Dict[str, Any],
        valuation_date: Optional[datetime] = None,
        period: Optional[str] = None
    ) -> CompanyMetric:
        
        # 确保 input_params 存为 JSON 字符串，而不是 Python 的 dict 字符串表示
        input_params_str = json.dumps(inputs) if inputs else None
        
        metric = CompanyMetric(
            company_id=company_id,
            metric_code=metric_code,
            value=value,
            input_params=input_params_str,
            valuation_date=valuation_date,
            period=period
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric

    def get_latest_metric(self, db: Session, company_id: int, metric_code: str) -> Optional[CompanyMetric]:
        return db.query(CompanyMetric)\
            .filter(CompanyMetric.company_id == company_id, CompanyMetric.metric_code == metric_code)\
            .order_by(CompanyMetric.valuation_date.desc(), CompanyMetric.created_at.desc())\
            .first()

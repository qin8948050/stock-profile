from abc import ABC, abstractmethod
from typing import Dict, Any
from sqlalchemy.orm import Session

class ValuationStrategy(ABC):
    """所有估值指标计算策略的基类"""
    
    @property
    @abstractmethod
    def metric_code(self) -> str:
        """指标唯一代号，如 'PEG'"""
        pass

    @abstractmethod
    def calculate(self, company_id: int, inputs: Dict[str, Any], db: Session) -> float:
        """
        执行计算逻辑
        :param company_id: 公司ID
        :param inputs: 前端传入的手动参数
        :param db: 数据库会话 (用于查询系统已有数据)
        :return: 计算结果
        """
        pass

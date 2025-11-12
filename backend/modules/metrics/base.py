from abc import ABC, abstractmethod

class MetricsEngine(ABC):
    @abstractmethod
    def compute(self, data: dict) -> dict:
        """根据原始财务数据计算指标"""
        pass
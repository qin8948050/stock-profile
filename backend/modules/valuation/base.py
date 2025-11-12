from abc import ABC, abstractmethod

class ValuationModel(ABC):
    @abstractmethod
    def estimate(self, metrics: dict) -> float:
        """根据指标计算合理估值"""
        pass
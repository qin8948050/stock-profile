from abc import ABC, abstractmethod

class AIEngine(ABC):
    @abstractmethod
    def analyze(self, company_data: dict, metrics: dict, valuation: dict) -> str:
        """生成分析报告"""
        pass
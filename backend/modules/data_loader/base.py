from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load(self, company_code: str):
        """加载指定公司的原始数据"""
        pass
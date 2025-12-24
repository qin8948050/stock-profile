from enum import Enum

class ValuationMetricType(str, Enum):
    PEG = "PEG"
    DCF = "DCF"
    # 未来可以添加更多，如:
    # ROE_VALUATION = "ROE_VALUATION"

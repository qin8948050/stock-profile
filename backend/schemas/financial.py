from enum import Enum
from typing import Optional, Dict, Any

from pydantic import BaseModel


class FinancialStatementType(str, Enum):
    """Enumeration for the type of financial statement."""
    BALANCE = "balance"
    CASH = "cash"
    INCOME = "income"


class FinancialBase(BaseModel):
    company_id: Optional[int] = None


class FinancialSheetUpsert(FinancialBase):
    type: FinancialStatementType
    period: Optional[str] = None


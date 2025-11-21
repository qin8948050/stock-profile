from enum import Enum
from typing import Optional, Dict, Any

from fastapi import Form
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
    fiscalYear: Optional[str] = None


class StatementUploadForm:
    """Dependency class to handle form fields for file uploads."""
    def __init__(
        self,
        company_id: int = Form(...),
        type: FinancialStatementType = Form(...),
    ):
        self.company_id = company_id
        self.type = type
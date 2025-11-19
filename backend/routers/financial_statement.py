from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.financial_repo import BalanceStatementRepository
from schemas.financial import FinancialSheetUpsert, FinancialStatementType
from schemas.response import ApiResponse

router = APIRouter(prefix="/financial-statements", tags=["Financial Statements"])



def get_financial_repo(statement_type: FinancialStatementType):
    repo_map = {
        FinancialStatementType.BALANCE: BalanceStatementRepository(),
    }
    repo = repo_map.get(statement_type)
    if repo is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid financial statement type: {statement_type}")
    return repo

@router.post("/", response_model=ApiResponse)
def upsert_financial_statement(financial_statement_in: FinancialSheetUpsert, db: Session = Depends(get_db)):
    repo = get_financial_repo(financial_statement_in.type)
    new_financial_data = repo.create(db=db, obj_in=financial_statement_in)
    return ApiResponse.success(data=new_financial_data)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.response import ApiResponse
from schemas.valuation import ValuationRequest, ValuationResponse
from services.valuation_service import ValuationService

router = APIRouter(
    prefix="/valuation",
    tags=["valuation"]
)

@router.post("/companies/{company_id}/calculate", response_model=ApiResponse[ValuationResponse])
def calculate_valuation_metric(
    company_id: int, 
    request: ValuationRequest, 
    db: Session = Depends(get_db)
):
    """
    计算并保存估值指标 (如 PEG, DCF 等)
    """
    service = ValuationService(db)
    try:
        data = service.calculate_and_save(
            company_id, 
            request.metric_code, 
            request.inputs
        )
        return ApiResponse.success(data=data)
    except ValueError as e:
        # 捕获业务层的 ValueError，转换为 400 Bad Request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # 捕获其他未预期的错误，转换为 500 Internal Server Error (可选，FastAPI 默认也会处理)
        print(f"Unexpected error: {e}") # 建议使用 logger
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while calculating the metric."
        )

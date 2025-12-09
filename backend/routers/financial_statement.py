import json
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session

from core.database import get_db
from repositories import CompanyRepository, get_company_repo
from repositories.financial_repo import get_statement_dependencies
from schemas.chart import ChartData
from schemas.financial import FinancialSheetUpsert, StatementUploadForm, FinancialStatementType
from schemas.response import ApiResponse
from services.financial_service import FinancialMetricService

router = APIRouter(prefix="/financial-statements", tags=["Financial Statements"])


@router.get("/financial-metric", response_model=ApiResponse[ChartData])
def get_financial_metric(
    company_id: int = Query(..., description="The ID of the company"),
    metric_name: str = Query(..., description="The name of the financial metric (e.g., 'total_revenue')"),
    service: FinancialMetricService = Depends(FinancialMetricService),
):
    """
    Get financial metric data for a company, formatted for charting.
    
    This endpoint relies on the global exception handlers to manage errors.
    - Expected errors (e.g., metric not found) are raised as HTTExceptions from the service layer.
    - Unexpected errors are caught by the generic exception handler and returned as a 500 response.
    """
    chart_data = service.get_metric_chart_data(company_id, metric_name)
    return ApiResponse.success(data=chart_data)


@router.post("/upload", response_model=ApiResponse)
async def upload_and_upsert_financial_statement(
    db: Session = Depends(get_db),
    company_repo: CompanyRepository = Depends(get_company_repo),
    form_data: StatementUploadForm = Depends(),
    file: UploadFile = File(..., description="JSON文件"),
):
    """
    通过上传JSON文件来更新或插入（upsert）财务报表数据。
    """
    # 1. 校验公司是否存在
    company = company_repo.get(db, id=form_data.company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {form_data.company_id} not found."
        )

    # 2. 校验文件类型
    if not file.filename.endswith('.json'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a .json file."
        )

    # 3. 获取报表类型对应的 repo
    try:
        _, repo = get_statement_dependencies(form_data.type)
    except HTTPException as e:
        raise e

    # 4. 读取并解析JSON文件
    contents = await file.read()
    try:
        data = json.loads(contents)
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON format in the uploaded file.")

    # 5. 执行 upsert 操作
    new_financial_data = repo.upsert_from_json(db=db, company_id=form_data.company_id, data=data)
    return ApiResponse.success(data=new_financial_data)

@router.post("/", response_model=ApiResponse)
def upsert_financial_statement(
    financial_statement_in: FinancialSheetUpsert,
    db: Session = Depends(get_db),
    company_repo: CompanyRepository = Depends(get_company_repo),
):
    """
    Fetches financial data from an external API and upserts it into the database.
    """
    company = company_repo.get(db, id=financial_statement_in.company_id)
    if not company or not company.ticker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {financial_statement_in.company_id} not found or has no ticker symbol."
        )

    # 2. 获取报表类型对应的 loader 和 repo
    try:
        loader, repo = get_statement_dependencies(financial_statement_in.type)
    except HTTPException as e:
        raise e


    data = loader.load(company.ticker)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not fetch financial data for symbol '{company.ticker}'. "
                   f"The symbol might be invalid or the API is unavailable."
        )

    # 4. 执行 upsert 操作
    new_financial_data = repo.upsert_from_json(db=db, company_id=financial_statement_in.company_id, data=data)
    return ApiResponse.success(data=new_financial_data)

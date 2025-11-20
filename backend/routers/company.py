from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas import CompanyCreate, CompanyUpdate, CompanyInDB
from schemas.pagination import Page
from repositories import CompanyRepository, get_company_repo
from core.database import get_db
from core.pagination import paginate
from schemas.response import ApiResponse

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=ApiResponse[CompanyInDB])
def create_company(company_in: CompanyCreate, db: Session = Depends(get_db), repo: CompanyRepository = Depends(get_company_repo)):
    new_company=repo.create(db=db, obj_in=company_in)
    return ApiResponse.success(data=new_company)

@router.get("/{company_id}", response_model=ApiResponse[CompanyInDB])
def get_company(company_id: int, db: Session = Depends(get_db), repo: CompanyRepository = Depends(get_company_repo)):
    db_obj = repo.get(db, id=company_id)
    if not db_obj:
        return ApiResponse.error(msg="Company not found", status=404)
    return ApiResponse.success(data=db_obj)

@router.get("/", response_model=ApiResponse[Page[CompanyInDB]])
def list_companies(skip: int = 1, limit: int = 100, db: Session = Depends(get_db), repo: CompanyRepository = Depends(get_company_repo)):
    paginated_data = paginate(
        db=db,
        repo=repo,
        response_schema=CompanyInDB,
        skip=skip,
        limit=limit
    )
    return ApiResponse.success(data=paginated_data)

@router.put("/{company_id}", response_model=ApiResponse[CompanyInDB])
def update_company(company_id: int, company_in: CompanyUpdate, db: Session = Depends(get_db), repo: CompanyRepository = Depends(get_company_repo)):
    db_obj = repo.get(db, id=company_id)
    if not db_obj:
        return ApiResponse.error(msg="Company not found", status=404)
    
    updated_company = repo.update(db=db, db_obj=db_obj, obj_in=company_in)
    return ApiResponse.success(data=updated_company)

@router.delete("/{company_id}", response_model=ApiResponse)
def delete_company(company_id: int, db: Session = Depends(get_db), repo: CompanyRepository = Depends(get_company_repo)):
    deleted_obj = repo.delete(db, id=company_id)
    if not deleted_obj:
        return ApiResponse.error(msg="Company not found", status=404)
    return ApiResponse.success(msg=f"Company with id {company_id} deleted successfully.")
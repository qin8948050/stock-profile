from typing import TypeVar,Type
from sqlalchemy.orm import Session
from pydantic import BaseModel
from schemas.pagination import Page

T = TypeVar("T", bound=BaseModel)


def paginate(
    *,
    db: Session,
    repo,  # The repository instance
    response_schema: Type[T],
    skip: int = 1,
    limit: int = 100,
) -> Page[T]:

    offset = (skip - 1) * limit
    items = repo.list(db, skip=offset, limit=limit)
    total = repo.count(db)
    total_pages = (total + limit - 1) // limit if limit > 0 else 0

    # Pydantic v2 会自动验证 items 是否符合 response_schema
    return Page[response_schema](items=items, page=skip, total_pages=total_pages, total=total)
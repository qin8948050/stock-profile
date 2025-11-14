from pydantic import BaseModel
from typing import List, TypeVar, Generic

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    items: List[T]
    page: int
    total_pages: int
    total: int

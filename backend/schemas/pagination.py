from pydantic import BaseModel, ConfigDict
from typing import List, TypeVar, Generic

ItemType = TypeVar('ItemType')

class Page(BaseModel, Generic[ItemType]):
    items: List[ItemType]
    page: int
    total_pages: int
    total: int
    # 允许 Pydantic 模型从 ORM 对象属性创建
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel
from datetime import datetime


class BaseSchema(BaseModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
from datetime import datetime, timezone, timedelta

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# 定义东八区时区对象
CST = timezone(timedelta(hours=8))

def now_cst():
    """返回当前东八区时间"""
    return datetime.now(CST)

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=now_cst)
    updated_at = Column(DateTime(timezone=True), default=now_cst, onupdate=now_cst)
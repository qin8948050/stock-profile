import logging
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.log import logger
from models import Base
from core.config import config

# -----------------------------
# 数据库配置
# -----------------------------
DB_USER = config.database.user
DB_PASSWORD = config.database.password
DB_HOST = config.database.host
DB_PORT = config.database.port
DB_NAME = config.database.name

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

# -----------------------------
# 创建数据库引擎
# -----------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True,            # 开发环境日志可见 SQL
    pool_pre_ping=True,   # 检查连接有效性（防止断连）
    future=True           # 启用 SQLAlchemy 2.0 风格
)

# -----------------------------
# 创建 SessionLocal
# -----------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # ✅ 防止提交后对象过期
)

# -----------------------------
# FastAPI 依赖注入（推荐方式）
# -----------------------------
def get_db():
    """
    用于 FastAPI 路由依赖：
    db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# 初始化数据库（仅启动时调用一次）
# -----------------------------
def init_db():
    """
    在 main.py 启动事件中调用：
        from backend.database import init_db
        @app.on_event("startup")
        def startup():
            init_db()
    """
    logger.info("✅ 初始化数据库表结构中...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ 数据库初始化完成")

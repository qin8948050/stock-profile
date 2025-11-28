from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.log import logger
from core.database import init_db, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI's lifespan event manager.
    """
    logger.info("🚀 Application starting up... Initializing database.")
    init_db()  # Automatically import models and create tables (checkfirst=True)
    yield
    logger.info("🛑 Application shutting down... Cleaning up resources.")

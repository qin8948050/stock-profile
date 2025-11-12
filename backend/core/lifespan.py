from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.log import logger
from core.telemetry import setup_tracer
from core.database import init_db, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI's lifespan event manager.
    """
    logger.info("🚀 Application starting up... Initializing telemetry and database.")
    setup_tracer(app=app, engine=engine)
    init_db()  # Automatically import models and create tables (checkfirst=True)
    yield
    logger.info("🛑 Application shutting down... Cleaning up resources.")

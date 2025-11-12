import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider # type: ignore
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from core.config import config

def setup_tracer(app=None, engine=None):
    """
    初始化 OpenTelemetry Tracing（OTLP / Jaeger）
    """
    # 定义服务元信息
    resource = Resource.create({
        "service.name": config.app.name,
        "service.version": config.app.version,
        "deployment.environment": config.opentelemetry.deployment_environment,
    })

    # 初始化 TracerProvider
    provider = TracerProvider(resource=resource)

    # OTLP 导出（可以是 Jaeger Collector / OTLP endpoint）
    exporter = OTLPSpanExporter(endpoint=config.opentelemetry.otlp_endpoint, timeout=10)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    # 设置全局 TracerProvider
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(config.app.name)

    # 自动为 FastAPI / SQLAlchemy / Logging 注入
    if app:
        FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    if engine:
        SQLAlchemyInstrumentor().instrument(engine=engine)
    LoggingInstrumentor().instrument(set_logging_format=True)

    return tracer

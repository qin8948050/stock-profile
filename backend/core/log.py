from pathlib import Path
from rich.logging import RichHandler
from logging.handlers import RotatingFileHandler
import json
import os
import logging
from datetime import datetime, timezone, timedelta


logger = logging.getLogger()

class JsonFormatter(logging.Formatter):
    """格式化为 JSON 的日志输出"""

    def __init__(self, fmt_dict: dict = None):
        self.fmt_dict = fmt_dict or {
            "level": "levelname",
            "message": "message",
            "loggerName": "name",
            "processName": "processName",
            "processID": "process",
            "threadName": "threadName",
            "threadID": "thread",
            "@timestamp": "asctime"
        }

    def usesTime(self) -> bool:
        return "@timestamp" in self.fmt_dict.values() or "asctime" in self.fmt_dict.values()

    def formatTime(self, record, datefmt=None) -> str:
        """东八区时间，格式 2025-10-27 18:19:20,227"""
        dt = datetime.fromtimestamp(record.created, tz=timezone(timedelta(hours=8)))
        return dt.strftime("%Y-%m-%d %H:%M:%S,") + f"{int(record.msecs):03d}"

    def formatMessage(self, record) -> dict:
        return {k: getattr(record, v, None) for k, v in self.fmt_dict.items()}

    def format(self, record) -> str:
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record)

        message_dict = self.formatMessage(record)

        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        # 检查并添加 OpenTelemetry 的 trace 信息
        # LoggingInstrumentor 会将这些属性添加到 LogRecord 中
        # 增加健壮性：ID 可能已经是字符串（来自 loguru），也可能是整数（来自 logging）
        trace_id = getattr(record, "otelTraceID", 0)
        if trace_id:
            # 如果是整数，格式化为32位十六进制；如果是字符串，直接使用
            message_dict["trace_id"] = format(trace_id, "032x") if isinstance(trace_id, int) else trace_id

        span_id = getattr(record, "otelSpanID", 0)
        if span_id:
            message_dict["span_id"] = format(span_id, "016x") if isinstance(span_id, int) else span_id

        # 添加应用信息
        message_dict.setdefault("app_name", os.getenv("service_name", "stock-profile"))
        message_dict.setdefault("app_port", os.getenv("app_port", "8080"))

        return json.dumps(message_dict, ensure_ascii=False, default=str)

def init_log(log_level: str = "INFO", log_file: Path = None):
    """初始化全局日志配置"""
    log_level_value = getattr(logging, log_level.upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level_value)

    # ✅ 清除旧的 handler，防止重复输出
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)

    # 控制台日志（美化输出）
    # 使用 RichHandler 并移除默认格式，让日志消息直接通过
    console_handler = RichHandler(
        rich_tracebacks=True,
        show_path=False,
        markup=True,  # 启用 markup 功能，可以在日志消息中使用 [bold green]...[/] 语法
        keywords=[
            "GET", "POST", "PUT", "DELETE",  # HTTP 方法
            "client=", "method=", "path=", "status_code=", "time=", # 访问日志关键字
            "ERROR", "CRITICAL" # 错误级别
        ],
    )
    root_logger.addHandler(console_handler)

    # 文件日志（JSON 格式）
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(log_file, mode='a', maxBytes=100 * 1024 * 1024, backupCount=5, encoding="utf-8")
        file_handler.setFormatter(JsonFormatter({
            "level": "levelname",
            "message": "message",
            "logger_name": "name",
            "process_name": "processName",
            "process_id": "process",
            "thread_name": "threadName",
            "thread_id": "thread",
            "@timestamp": "asctime"
        }))
        root_logger.addHandler(file_handler)

    # ✅ 捕获 uvicorn 和 fastapi 的日志
    # 将它们的 handler 清空，并设置 propagate=True，让日志事件冒泡到 root logger
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
        logging.getLogger(name).handlers.clear()
        logging.getLogger(name).propagate = True

    root_logger.info(f"Logger configured, level={log_level}")
    if log_file:
        root_logger.info(f"Log file path: {log_file}")
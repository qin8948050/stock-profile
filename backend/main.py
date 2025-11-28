from pathlib import Path
import uvicorn

from core.app_factory import create_app
from core.config import config
from core.log import init_log


# 初始化应用日志系统
init_log(log_level=config.logging.level, log_file=Path(config.logging.file))

# 使用工厂函数创建应用实例
app = create_app()

# 启动入口（支持直接运行）
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.server.host,
        port=config.app.port,
        reload=config.server.reload,
        log_level=config.server.log_level.lower(),
        access_log=False  # 禁用 uvicorn 默认的访问日志
    )
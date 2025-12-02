# 使用官方的 Python 运行时作为父镜像
FROM cowell-images.tencentcloudcr.com/cowellpi/python:3.12-ubuntu

# 设置环境变量，防止 Python 写入 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE 1
# 确保 Python 输出是无缓冲的
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

# 安装诗歌 (Poetry) 或 pip，这里我们使用 pip
# 首先复制依赖文件
COPY ../requirements.txt /app/requirements.txt

# 安装项目依赖
# --no-cache-dir: 不缓存包，减小镜像体积
# --upgrade pip: 升级 pip 到最新版本
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --no-cache-dir --upgrade pip && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --no-cache-dir -r /app/requirements.txt

# 将你的后端代码复制到工作目录中
COPY . /app

# 暴露端口 8000，以便容器外可以访问
EXPOSE 8000

# 容器启动时运行的命令
# 假设你的 FastAPI 实例在 main.py 文件中的 app 变量
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
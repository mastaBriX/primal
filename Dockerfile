# 第一阶段：构建阶段
FROM python:3.11-alpine AS builder

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    build-base

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 升级 pip
RUN pip install --upgrade pip

# 复制项目配置文件
COPY pyproject.toml .

# 复制源代码（用于安装依赖）
COPY src/ ./src/

# 安装项目依赖（pip 会从 pyproject.toml 读取依赖）
RUN pip install --no-cache-dir .

# 第二阶段：运行阶段
FROM python:3.11-alpine AS runner

RUN apk add --no-cache libffi

# 创建非 root 用户
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=src.app \
    FLASK_DEBUG=false \
    FLASK_HOST=0.0.0.0 \
    PORT=5000 \
    MAX_INPUT_VALUE=1000000000 \
    TIMEOUT_SECONDS=5 \
    LOG_LEVEL=INFO \
    PYTHONPATH=/app

# 从构建阶段复制 Python 包
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制源代码（包含模板和配置文件）
COPY src/ ./src/

# 更改文件所有权
RUN chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

EXPOSE 5000

# 使用 gunicorn 运行应用（生产环境）
CMD ["gunicorn", "--config", "src/gunicorn.conf.py", "src.app:app"]
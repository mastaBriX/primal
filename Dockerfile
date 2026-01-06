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

# 复制项目配置文件和应用代码（用于安装依赖）
COPY pyproject.toml .
COPY app.py .

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
    FLASK_APP=app.py

# 从构建阶段复制 Python 包
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制应用代码
COPY app.py .
COPY templates/ ./templates/

# 更改文件所有权
RUN chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
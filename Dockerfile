# ============================================
# 第一阶段：构建阶段
# ============================================
FROM python:3.11-alpine AS builder

# 安装构建依赖（合并命令减少层数）
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    build-base \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

# 设置工作目录和环境变量
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 复制并安装依赖
COPY requirements.txt .
RUN pip install --user --no-warn-script-location --no-compile -r requirements.txt \
    && find /root/.local -type f -name "*.pyc" -delete \
    && find /root/.local -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true \
    && find /root/.local -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true \
    && find /root/.local -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true \
    && find /root/.local -type d -name "test" -exec rm -rf {} + 2>/dev/null || true

# ============================================
# 第二阶段：运行阶段（最小化镜像）
# ============================================
FROM python:3.11-alpine AS runner

# 安装最小运行时依赖并清理不必要的文件
RUN apk add --no-cache libffi \
    && rm -rf /var/cache/apk/* \
    && rm -rf /usr/lib/python3.11/ensurepip \
    && rm -rf /usr/lib/python3.11/__pycache__ \
    && rm -rf /usr/lib/python3.11/lib2to3 \
    && rm -rf /usr/lib/python3.11/distutils \
    && rm -rf /usr/lib/python3.11/idlelib \
    && rm -rf /usr/lib/python3.11/turtledemo \
    && rm -rf /usr/lib/python3.11/test \
    && rm -rf /usr/lib/python3.11/unittest \
    && rm -rf /usr/lib/python3.11/pydoc_data \
    && rm -rf /usr/lib/python3.11/doctest.py \
    && rm -rf /usr/lib/python3.11/tkinter \
    && find /usr/lib/python3.11 -name "*.pyc" -delete \
    && find /usr/lib/python3.11 -name "*.pyo" -delete \
    && find /usr/lib/python3.11 -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true \
    && find /usr/lib/python3.11 -name "test_*.py" -delete \
    && find /usr/lib/python3.11 -name "*_test.py" -delete

# 设置工作目录和环境变量
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app.py \
    PATH=/app/.local/bin:$PATH

# 创建非 root 用户（合并命令）
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# 从构建阶段复制已安装的 Python 包（仅必要的文件）
COPY --from=builder --chown=appuser:appuser /root/.local /app/.local

# 复制应用代码
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser templates/ ./templates/

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 5000

# 健康检查（使用 Python 内置模块）
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# 运行应用
CMD ["python", "app.py"]


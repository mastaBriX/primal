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

# 复制依赖文件
COPY requirements.txt .

# 安装到系统目录（不使用 --user）
RUN pip install -r requirements.txt

# 第二阶段：运行阶段
FROM python:3.11-alpine AS runner

RUN apk add --no-cache libffi

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

EXPOSE 5000

CMD ["python", "app.py"]
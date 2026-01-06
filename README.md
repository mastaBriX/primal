# 质数判断工具

一个带有Web界面的质数判断程序，支持超时保护机制。

## 功能特点

- 🌐 现代化的Web用户界面
- ⚡ 高效的质数判断算法（优化到√n）
- ⏱️ 5秒超时保护，防止大数计算导致卡死
- 📱 响应式设计，支持移动设备

## 安装步骤

### 方式1：使用 uv（推荐，快速且高效）

```bash
# 安装 uv（如果尚未安装）
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步依赖（安装生产依赖）
uv sync

# 安装包含测试依赖
uv sync --extra test
```

### 方式2：使用 pip 和 pyproject.toml

```bash
# 安装生产依赖
pip install -e .

# 或安装包含测试依赖
pip install -e ".[test]"
```

### 方式3：使用 requirements.txt（传统方式）

```bash
pip install -r requirements.txt
```

## 运行程序

### 使用 uv

```bash
# 使用 uv 运行（自动使用虚拟环境）
uv run python app.py
```

### 使用传统方式

```bash
python app.py
```

然后在浏览器中访问：http://localhost:5000

## 本地测试

### 使用 uv（推荐）

```bash
# 运行所有测试
uv run pytest tests/ -v

# 带覆盖率报告
uv run pytest tests/ -v --cov=app --cov-report=term-missing
```

### 使用传统方式

```bash
# 如果已安装测试依赖
pytest tests/ -v

# 或带覆盖率报告
pytest tests/ -v --cov=app --cov-report=term-missing
```

### 运行特定测试文件

```bash
pytest tests/test_app.py -v
```

### 运行特定测试类或函数

```bash
# 运行特定测试类
pytest tests/test_app.py::TestIsPrime -v

# 运行特定测试函数
pytest tests/test_app.py::TestIsPrime::test_is_prime_small_primes -v
```

### 测试输出说明

- `-v` 或 `--verbose`：显示详细输出
- `--cov=app`：生成代码覆盖率报告
- `--cov-report=term-missing`：在终端显示覆盖率，并标记未覆盖的行

## 使用说明

1. 在输入框中输入一个非负整数
2. 点击"判断质数"按钮或按回车键
3. 程序会在5秒内返回结果：
   - 绿色：是质数
   - 黄色：不是质数
   - 红色：错误或超时

## Docker 部署

### 使用 Docker Compose（推荐）

Docker Compose 配置会从 GitHub Container Registry 拉取预构建的公开镜像。

```bash
# 拉取最新镜像并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 更新到最新镜像
docker-compose pull && docker-compose up -d
```

然后在浏览器中访问：http://localhost:5000

**注意**：镜像已设置为公开，无需登录即可拉取。

### 使用 Docker 命令

#### 直接运行

```bash
docker run -d -p 5000:5000 --name primal-checker ghcr.io/mastabrix/primal:latest
```

#### 本地构建（可选）

```bash
docker build -t primal-checker .
docker run -d -p 5000:5000 --name primal-checker primal-checker
```

## CI/CD

项目配置了 GitHub Actions 工作流，在以下情况会自动构建 Docker 镜像：

- 推送到 `main` 或 `master` 分支
- 创建版本标签（如 `v1.0.0`）
- 手动触发工作流

构建的镜像会自动推送到 GitHub Container Registry (ghcr.io)。

## 技术实现

- **后端**：Flask Web框架
- **超时机制**：使用Python threading模块实现超时控制
- **算法优化**：只检查到√n，提高计算效率
- **容器化**：Docker 支持，便于部署
- **CI/CD**：GitHub Actions 自动构建镜像


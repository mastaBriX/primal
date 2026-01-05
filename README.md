# 质数判断工具

一个带有Web界面的质数判断程序，支持超时保护机制。

## 功能特点

- 🌐 现代化的Web用户界面
- ⚡ 高效的质数判断算法（优化到√n）
- ⏱️ 5秒超时保护，防止大数计算导致卡死
- 📱 响应式设计，支持移动设备

## 安装步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python app.py
```

然后在浏览器中访问：http://localhost:5000

## 使用说明

1. 在输入框中输入一个非负整数
2. 点击"判断质数"按钮或按回车键
3. 程序会在5秒内返回结果：
   - 绿色：是质数
   - 黄色：不是质数
   - 红色：错误或超时

## Docker 部署

### 构建镜像

```bash
docker build -t primal-checker .
```

### 运行容器

```bash
docker run -d -p 5000:5000 --name primal-checker primal-checker
```

然后在浏览器中访问：http://localhost:5000

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


"""
Gunicorn 配置文件
用于生产环境部署
"""
import multiprocessing
import os

# 服务器配置
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
worker_connections = 1000
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '30'))
keepalive = 2

# 日志配置
accesslog = "-"  # 输出到 stdout
errorlog = "-"   # 输出到 stderr
loglevel = os.environ.get('LOG_LEVEL', 'info').lower()

# 进程配置
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# 性能配置
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

def when_ready(server):
    """服务器就绪时的回调"""
    server.log.info("Gunicorn server is ready. Spawning workers")

def worker_int(worker):
    """工作进程中断时的回调"""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """工作进程 fork 前的回调"""
    pass

def post_fork(server, worker):
    """工作进程 fork 后的回调"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    """工作进程初始化后的回调"""
    pass

def worker_abort(worker):
    """工作进程异常退出时的回调"""
    worker.log.info("Worker received SIGABRT signal")


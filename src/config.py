"""
应用配置模块
支持通过环境变量配置常用设置
"""
import os
import secrets


class Config:
    """应用配置类"""
    
    # Flask 配置
    SECRET_KEY: str = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    DEBUG: bool = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST: str = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT: int = int(os.environ.get('PORT', '5000'))
    
    # 应用配置
    FLASK_APP: str = os.environ.get('FLASK_APP', 'app.py')
    
    # 质数检查配置
    MAX_INPUT_VALUE: int = int(os.environ.get('MAX_INPUT_VALUE', '1000000000'))  # 默认10亿
    TIMEOUT_SECONDS: int = int(os.environ.get('TIMEOUT_SECONDS', '5'))  # 默认5秒
    
    # 日志配置
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = os.environ.get(
        'LOG_FORMAT', 
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Gunicorn 配置
    GUNICORN_WORKERS: int = int(os.environ.get('GUNICORN_WORKERS', '0'))  # 0 表示自动计算
    GUNICORN_TIMEOUT: int = int(os.environ.get('GUNICORN_TIMEOUT', '30'))
    
    @classmethod
    def get_config_dict(cls) -> dict:
        """获取 Flask 配置字典"""
        return {
            'SECRET_KEY': cls.SECRET_KEY,
            'DEBUG': cls.DEBUG,
        }
    
    @classmethod
    def validate(cls) -> None:
        """验证配置的有效性"""
        if cls.MAX_INPUT_VALUE < 1:
            raise ValueError("MAX_INPUT_VALUE 必须大于 0")
        if cls.TIMEOUT_SECONDS < 1:
            raise ValueError("TIMEOUT_SECONDS 必须大于 0")
        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError("PORT 必须在 1-65535 之间")
    
    @classmethod
    def __repr__(cls) -> str:
        """配置的字符串表示"""
        return (
            f"Config(DEBUG={cls.DEBUG}, PORT={cls.PORT}, "
            f"MAX_INPUT_VALUE={cls.MAX_INPUT_VALUE:,}, "
            f"TIMEOUT_SECONDS={cls.TIMEOUT_SECONDS})"
        )


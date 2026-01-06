"""
Flask 应用主文件
路由层直接调用服务层
"""
from flask import Flask, render_template, request, jsonify
from flask_talisman import Talisman
import logging
import os
from src.config import Config
from src.services.prime_checker import PrimeChecker


# 创建 Flask 应用
# 模板目录在 src/templates/ 下
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)

# 配置安全响应头
# 在生产环境启用严格的安全策略，开发环境和测试环境可以放宽
# 检查是否在测试环境中（通过环境变量）
is_testing = os.environ.get('FLASK_ENV') == 'testing' or os.environ.get('PYTEST_CURRENT_TEST') is not None

if Config.DEBUG or is_testing:
    # 开发/测试环境：允许内联脚本和样式（用于调试和测试），不强制 HTTPS
    Talisman(
        app,
        force_https=False,
        strict_transport_security=False,
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline'",
            'style-src': "'self' 'unsafe-inline'",
        }
    )
else:
    # 生产环境：严格的安全策略
    Talisman(
        app,
        force_https=True,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,  # 1年
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self'",
            'style-src': "'self'",
            'img-src': "'self' data:",
            'font-src': "'self'",
        },
        referrer_policy='strict-origin-when-cross-origin',
        feature_policy={
            'geolocation': "'none'",
            'notifications': "'none'",
        }
    )

# 配置应用
app.config.update(Config.get_config_dict())

# 设置日志
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# 验证配置
Config.validate()

# 创建服务实例
prime_checker = PrimeChecker()


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_prime():
    """检查质数的API端点"""
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({
                'success': False,
                'message': '请求体不能为空'
            }), 400
        
        # 验证请求数据
        number_str = str(data.get('number', '')).strip()
        
        if not number_str:
            return jsonify({
                'success': False,
                'message': '请输入一个数字'
            }), 400
        
        try:
            number = int(number_str)
        except ValueError:
            return jsonify({
                'success': False,
                'message': '请输入有效的整数'
            }), 400
        
        if number < 0:
            return jsonify({
                'success': False,
                'message': '请输入非负整数'
            }), 400
        
        # 调用服务层检查质数
        result = prime_checker.check(number)
        
        if not result.is_success():
            # 超时或错误（输入验证失败返回 400，其他返回 200）
            status_code = 400 if any(keyword in result.message for keyword in ['过大', '超过', '非负整数']) else 200
            return jsonify({
                'success': False,
                'message': result.message
            }), status_code
        
        return jsonify({
            'success': True,
            'is_prime': result.is_prime,
            'message': result.message,
            'number': result.number
        }), 200
        
    except Exception as e:
        # 记录详细错误到日志
        logger.error(f'服务器错误: {str(e)}', exc_info=True)
        
        # 生产环境返回通用错误消息
        if Config.DEBUG:
            error_message = f'服务器错误：{str(e)}'
        else:
            error_message = '服务器内部错误，请稍后重试'
        
        return jsonify({
            'success': False,
            'message': error_message
        }), 500


if __name__ == '__main__':
    logger.info(f'启动应用 - Debug模式: {Config.DEBUG}, 端口: {Config.PORT}, 主机: {Config.HOST}')
    logger.info(f'配置: {Config}')
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

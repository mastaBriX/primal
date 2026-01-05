from flask import Flask, render_template, request, jsonify
import threading

app = Flask(__name__)

class TimeoutError(Exception):
    """自定义超时异常"""
    pass

def timeout_handler(signum, frame):
    """信号处理函数，用于超时"""
    raise TimeoutError("计算超时")

def is_prime(n, timeout_seconds=5):
    """
    判断一个数是否为质数，带超时保护
    
    Args:
        n: 要判断的数
        timeout_seconds: 超时时间（秒）
    
    Returns:
        tuple: (是否为质数, 消息)
    """
    if n < 2:
        return False, "质数必须大于等于2"
    
    if n == 2:
        return True, "2是质数"
    
    if n % 2 == 0:
        return False, f"{n}不是质数（能被2整除）"
    
    # 使用线程和超时机制
    result = [None]
    error = [None]
    
    def check_prime():
        try:
            # 优化：只需要检查到sqrt(n)
            import math
            sqrt_n = int(math.sqrt(n)) + 1
            
            for i in range(3, sqrt_n, 2):
                if n % i == 0:
                    result[0] = (False, f"{n}不是质数（能被{i}整除）")
                    return
            result[0] = (True, f"{n}是质数")
        except Exception as e:
            error[0] = str(e)
    
    # 创建线程执行质数检查
    thread = threading.Thread(target=check_prime)
    thread.daemon = True
    thread.start()
    thread.join(timeout=timeout_seconds)
    
    if thread.is_alive():
        return None, f"计算超时（超过{timeout_seconds}秒），数字可能过大"
    
    if error[0]:
        return None, f"计算出错：{error[0]}"
    
    return result[0]

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_prime():
    """检查质数的API端点"""
    try:
        data = request.get_json()
        number_str = data.get('number', '').strip()
        
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
        
        # 检查质数（带5秒超时）
        is_prime_result, message = is_prime(number, timeout_seconds=5)
        
        if is_prime_result is None:
            # 超时或错误
            return jsonify({
                'success': False,
                'message': message
            }), 200
        
        return jsonify({
            'success': True,
            'is_prime': is_prime_result,
            'message': message,
            'number': number
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'服务器错误：{str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


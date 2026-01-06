"""
质数检查服务模块
提供面向对象的质数检查功能
"""
import threading
import math
import logging
from typing import Optional, Tuple
from src.config import Config


logger = logging.getLogger(__name__)


class PrimeCheckResult:
    """质数检查结果类"""
    
    def __init__(self, is_prime: Optional[bool], message: str, number: int):
        """
        初始化检查结果
        
        Args:
            is_prime: 是否为质数（None 表示超时或错误）
            message: 结果消息
            number: 检查的数字
        """
        self.is_prime = is_prime
        self.message = message
        self.number = number
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'is_prime': self.is_prime,
            'message': self.message,
            'number': self.number
        }
    
    def is_success(self) -> bool:
        """检查是否成功完成（非超时/错误）"""
        return self.is_prime is not None


class PrimeChecker:
    """质数检查服务类"""
    
    def __init__(self, timeout_seconds: Optional[int] = None, max_value: Optional[int] = None):
        """
        初始化质数检查器
        
        Args:
            timeout_seconds: 超时时间（秒），默认使用配置值
            max_value: 最大输入值，默认使用配置值
        """
        self.timeout_seconds = timeout_seconds or Config.TIMEOUT_SECONDS
        self.max_value = max_value or Config.MAX_INPUT_VALUE
    
    def validate_input(self, number: int) -> Tuple[bool, Optional[str]]:
        """
        验证输入数字
        
        Args:
            number: 要验证的数字
            
        Returns:
            (是否有效, 错误消息)
        """
        if number < 0:
            return False, '请输入非负整数'
        
        if number > self.max_value:
            return False, f'输入数字过大，最大允许值为 {self.max_value:,}'
        
        return True, None
    
    def check(self, number: int) -> PrimeCheckResult:
        """
        检查数字是否为质数
        
        Args:
            number: 要检查的数字
            
        Returns:
            PrimeCheckResult: 检查结果
        """
        # 验证输入
        is_valid, error_msg = self.validate_input(number)
        if not is_valid:
            return PrimeCheckResult(None, error_msg, number)
        
        # 边界情况
        if number < 2:
            return PrimeCheckResult(False, "质数必须大于等于2", number)
        
        if number == 2:
            return PrimeCheckResult(True, "2是质数", number)
        
        if number % 2 == 0:
            return PrimeCheckResult(False, f"{number}不是质数（能被2整除）", number)
        
        # 使用线程和超时机制检查质数
        result = [None]
        error = [None]
        
        def check_prime():
            """在独立线程中检查质数"""
            try:
                sqrt_n = int(math.sqrt(number)) + 1
                
                for i in range(3, sqrt_n, 2):
                    if number % i == 0:
                        result[0] = (False, f"{number}不是质数（能被{i}整除）")
                        return
                result[0] = (True, f"{number}是质数")
            except Exception as e:
                error[0] = str(e)
                logger.error(f"质数检查出错: {e}", exc_info=True)
        
        # 创建线程执行质数检查
        thread = threading.Thread(target=check_prime)
        thread.daemon = True
        thread.start()
        thread.join(timeout=self.timeout_seconds)
        
        if thread.is_alive():
            return PrimeCheckResult(
                None,
                f"计算超时（超过{self.timeout_seconds}秒），数字可能过大",
                number
            )
        
        if error[0]:
            return PrimeCheckResult(
                None,
                f"计算出错：{error[0]}",
                number
            )
        
        is_prime, message = result[0]
        return PrimeCheckResult(is_prime, message, number)


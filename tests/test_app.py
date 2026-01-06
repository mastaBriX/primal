"""
测试 Flask 应用的质数检查功能
"""
import pytest
from src.app import app
from src.services.prime_checker import PrimeChecker


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def prime_checker():
    """创建质数检查器实例"""
    return PrimeChecker()


class TestPrimeChecker:
    """测试 PrimeChecker 类"""
    
    def test_check_small_primes(self, prime_checker):
        """测试小质数"""
        result = prime_checker.check(2)
        assert result.is_prime is True
        assert "2是质数" in result.message
        
        result = prime_checker.check(3)
        assert result.is_prime is True
        assert "3是质数" in result.message
        
        result = prime_checker.check(5)
        assert result.is_prime is True
        assert "5是质数" in result.message
        
        result = prime_checker.check(7)
        assert result.is_prime is True
        assert "7是质数" in result.message
        
        result = prime_checker.check(11)
        assert result.is_prime is True
        assert "11是质数" in result.message
        
        result = prime_checker.check(13)
        assert result.is_prime is True
        assert "13是质数" in result.message
        
        result = prime_checker.check(17)
        assert result.is_prime is True
        assert "17是质数" in result.message
        
        result = prime_checker.check(19)
        assert result.is_prime is True
        assert "19是质数" in result.message
    
    def test_check_small_composites(self, prime_checker):
        """测试小合数"""
        result = prime_checker.check(4)
        assert result.is_prime is False
        assert "4不是质数" in result.message
        
        result = prime_checker.check(6)
        assert result.is_prime is False
        assert "6不是质数" in result.message
        
        result = prime_checker.check(8)
        assert result.is_prime is False
        assert "8不是质数" in result.message
        
        result = prime_checker.check(9)
        assert result.is_prime is False
        assert "9不是质数" in result.message
        
        result = prime_checker.check(10)
        assert result.is_prime is False
        assert "10不是质数" in result.message
        
        result = prime_checker.check(15)
        assert result.is_prime is False
        assert "15不是质数" in result.message
    
    def test_check_edge_cases(self, prime_checker):
        """测试边界情况"""
        result = prime_checker.check(0)
        assert result.is_prime is False
        assert "质数必须大于等于2" in result.message
        
        result = prime_checker.check(1)
        assert result.is_prime is False
        assert "质数必须大于等于2" in result.message
        
        result = prime_checker.check(-1)
        assert result.is_prime is None
        assert "请输入非负整数" in result.message
    
    def test_check_larger_numbers(self, prime_checker):
        """测试较大的数字"""
        result = prime_checker.check(97)
        assert result.is_prime is True
        assert "97是质数" in result.message
        
        result = prime_checker.check(101)
        assert result.is_prime is True
        assert "101是质数" in result.message
        
        result = prime_checker.check(100)
        assert result.is_prime is False
        assert "100不是质数" in result.message
        
        result = prime_checker.check(1001)
        assert result.is_prime is False
        assert "1001不是质数" in result.message
    
    def test_validate_input(self, prime_checker):
        """测试输入验证"""
        is_valid, msg = prime_checker.validate_input(-1)
        assert is_valid is False
        assert "非负整数" in msg
        
        is_valid, msg = prime_checker.validate_input(1000000001)
        assert is_valid is False
        assert "过大" in msg or "超过" in msg
        
        is_valid, msg = prime_checker.validate_input(100)
        assert is_valid is True
        assert msg is None


class TestIndexRoute:
    """测试首页路由"""
    
    def test_index_route(self, client):
        """测试首页返回 200"""
        response = client.get('/')
        assert response.status_code == 200


class TestVersionRoute:
    """测试版本号 API 路由"""
    
    def test_version_route(self, client):
        """测试版本号 API 返回 200 和版本信息"""
        response = client.get('/api/version')
        assert response.status_code == 200
        data = response.get_json()
        assert 'version' in data
        assert isinstance(data['version'], str)
        assert len(data['version']) > 0


class TestCheckPrimeRoute:
    """测试质数检查 API 路由"""
    
    def test_check_prime_valid_prime(self, client):
        """测试检查有效的质数"""
        response = client.post('/check', 
                              json={'number': '7'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['is_prime'] is True
        assert '7是质数' in data['message']
        assert data['number'] == 7
    
    def test_check_prime_valid_composite(self, client):
        """测试检查有效的合数"""
        response = client.post('/check',
                              json={'number': '8'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['is_prime'] is False
        assert '8不是质数' in data['message']
        assert data['number'] == 8
    
    def test_check_prime_empty_number(self, client):
        """测试空数字"""
        response = client.post('/check',
                              json={'number': ''},
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert '请输入一个数字' in data['message']
    
    def test_check_prime_missing_number(self, client):
        """测试缺少数字字段"""
        response = client.post('/check',
                              json={},
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert '请输入一个数字' in data['message']
    
    def test_check_prime_invalid_number(self, client):
        """测试无效的数字格式"""
        response = client.post('/check',
                              json={'number': 'abc'},
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert '请输入有效的整数' in data['message']
    
    def test_check_prime_negative_number(self, client):
        """测试负数"""
        response = client.post('/check',
                              json={'number': '-5'},
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert '请输入非负整数' in data['message']
    
    def test_check_prime_zero(self, client):
        """测试零"""
        response = client.post('/check',
                              json={'number': '0'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['is_prime'] is False
        assert '质数必须大于等于2' in data['message']
    
    def test_check_prime_one(self, client):
        """测试一"""
        response = client.post('/check',
                              json={'number': '1'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['is_prime'] is False
        assert '质数必须大于等于2' in data['message']
    
    def test_check_prime_large_number(self, client):
        """测试大数字（超过限制）"""
        response = client.post('/check',
                              json={'number': '999999999999999999'},
                              content_type='application/json')
        # 大数字超过限制，应该返回 400
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert '过大' in data['message'] or '超过' in data['message']
    
    def test_check_prime_within_limit(self, client):
        """测试在限制内的较大数字"""
        response = client.post('/check',
                              json={'number': '999999999'},  # 9.99亿，在默认限制内
                              content_type='application/json')
        # 应该在限制内，可能超时或成功
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data

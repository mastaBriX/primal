"""
测试 Flask 应用的质数检查功能
"""
import pytest
from app import app, is_prime


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestIsPrime:
    """测试 is_prime 函数"""
    
    def test_is_prime_small_primes(self):
        """测试小质数"""
        assert is_prime(2) == (True, "2是质数")
        assert is_prime(3) == (True, "3是质数")
        assert is_prime(5) == (True, "5是质数")
        assert is_prime(7) == (True, "7是质数")
        assert is_prime(11) == (True, "11是质数")
        assert is_prime(13) == (True, "13是质数")
        assert is_prime(17) == (True, "17是质数")
        assert is_prime(19) == (True, "19是质数")
    
    def test_is_prime_small_composites(self):
        """测试小合数"""
        assert is_prime(4) == (False, "4不是质数（能被2整除）")
        assert is_prime(6) == (False, "6不是质数（能被2整除）")
        assert is_prime(8) == (False, "8不是质数（能被2整除）")
        assert is_prime(9) == (False, "9不是质数（能被3整除）")
        assert is_prime(10) == (False, "10不是质数（能被2整除）")
        assert is_prime(15) == (False, "15不是质数（能被3整除）")
    
    def test_is_prime_edge_cases(self):
        """测试边界情况"""
        assert is_prime(0) == (False, "质数必须大于等于2")
        assert is_prime(1) == (False, "质数必须大于等于2")
        assert is_prime(-1) == (False, "质数必须大于等于2")
    
    def test_is_prime_larger_numbers(self):
        """测试较大的数字"""
        assert is_prime(97) == (True, "97是质数")
        assert is_prime(101) == (True, "101是质数")
        assert is_prime(100) == (False, "100不是质数（能被2整除）")
        assert is_prime(1001) == (False, "1001不是质数（能被7整除）")


class TestIndexRoute:
    """测试首页路由"""
    
    def test_index_route(self, client):
        """测试首页返回 200"""
        response = client.get('/')
        assert response.status_code == 200


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
        """测试大数字（可能超时）"""
        response = client.post('/check',
                              json={'number': '999999999999999999'},
                              content_type='application/json')
        # 大数字可能会超时，但应该返回 200 而不是 500
        assert response.status_code == 200
        data = response.get_json()
        # 可能是超时或成功，但不应该是服务器错误
        assert 'success' in data


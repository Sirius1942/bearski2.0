"""智能断言推荐模块"""
import json
from typing import Dict, List, Any


class AssertionRecommender:
    """基于响应内容自动推荐断言"""
    
    @staticmethod
    def analyze_response(response: Dict[str, Any]) -> List[Dict[str, str]]:
        """分析响应并推荐断言
        
        Args:
            response: 响应数据字典
            
        Returns:
            推荐的断言列表
        """
        recommendations = []
        
        # 1. 状态码断言
        if 'status_code' in response:
            status = response['status_code']
            recommendations.append({
                'type': 'status_code',
                'assertion': f'assert response.status_code == {status}',
                'reason': f'验证 HTTP 状态码为 {status}'
            })
        
        # 2. 响应体结构断言
        if 'body' in response:
            body = response['body']
            
            # JSON 响应
            if isinstance(body, dict):
                # 检查必要字段
                for key in body.keys():
                    recommendations.append({
                        'type': 'field_exists',
                        'assertion': f'assert "{key}" in response.body',
                        'reason': f'验证字段 {key} 存在'
                    })
                
                # 检查字段类型
                for key, value in body.items():
                    value_type = type(value).__name__
                    recommendations.append({
                        'type': 'field_type',
                        'assertion': f'assert isinstance(response.body["{key}"], {value_type})',
                        'reason': f'验证字段 {key} 类型为 {value_type}'
                    })
                
                # 检查常见业务字段
                if 'code' in body:
                    recommendations.append({
                        'type': 'business_code',
                        'assertion': f'assert response.body["code"] == {body["code"]}',
                        'reason': '验证业务状态码'
                    })
                
                if 'success' in body:
                    recommendations.append({
                        'type': 'success_flag',
                        'assertion': f'assert response.body["success"] is {body["success"]}',
                        'reason': '验证成功标志'
                    })
                
                if 'data' in body:
                    recommendations.append({
                        'type': 'data_not_empty',
                        'assertion': 'assert response.body["data"] is not None',
                        'reason': '验证数据字段非空'
                    })
        
        # 3. 响应头断言
        if 'headers' in response:
            headers = response['headers']
            
            # Content-Type 检查
            if 'Content-Type' in headers:
                content_type = headers['Content-Type']
                recommendations.append({
                    'type': 'content_type',
                    'assertion': f'assert "{content_type}" in response.headers["Content-Type"]',
                    'reason': f'验证响应类型为 {content_type}'
                })
        
        # 4. 响应时间断言
        if 'duration' in response:
            duration = response['duration']
            threshold = 1000  # 默认 1 秒
            recommendations.append({
                'type': 'performance',
                'assertion': f'assert response.duration < {threshold}',
                'reason': f'验证响应时间小于 {threshold}ms'
            })
        
        return recommendations
    
    @staticmethod
    def generate_test_code(test_name: str, response: Dict[str, Any]) -> str:
        """生成完整的测试代码
        
        Args:
            test_name: 测试名称
            response: 响应数据
            
        Returns:
            测试代码字符串
        """
        recommendations = AssertionRecommender.analyze_response(response)
        
        code_lines = [
            f'def test_{test_name}():',
            '    """自动生成的测试用例"""',
            '    # TODO: 发送请求获取 response',
            '    ',
            '    # 推荐的断言'
        ]
        
        for rec in recommendations:
            code_lines.append(f'    # {rec["reason"]}')
            code_lines.append(f'    {rec["assertion"]}')
            code_lines.append('')
        
        return '\n'.join(code_lines)
    
    @staticmethod
    def save_recommendations(recommendations: List[Dict[str, str]], filepath: str):
        """保存推荐结果到文件
        
        Args:
            recommendations: 推荐列表
            filepath: 保存路径
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(recommendations, f, indent=2, ensure_ascii=False)

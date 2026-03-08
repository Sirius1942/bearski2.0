"""智能失败分析模块"""
import re
from typing import Dict, List

class AIAnalyzer:
    ERROR_PATTERNS = {
        'timeout': {
            'pattern': r'timeout|timed out',
            'diagnosis': '超时错误',
            'suggestions': ['增加等待时间', '检查网络', '优化性能']
        },
        'element_not_found': {
            'pattern': r'element not found|no such element',
            'diagnosis': '元素定位失败',
            'suggestions': ['检查定位器', '确认页面加载', '添加等待']
        },
        'assertion': {
            'pattern': r'assertion|expected.*but',
            'diagnosis': '断言失败',
            'suggestions': ['检查预期值', '验证数据格式', '确认业务逻辑']
        },
        'network': {
            'pattern': r'connection|network|refused',
            'diagnosis': '网络问题',
            'suggestions': ['检查服务状态', '验证URL', '检查防火墙']
        }
    }
    
    @staticmethod
    def analyze(error_message: str, step_name: str = '') -> Dict:
        result = {
            'error': error_message,
            'step': step_name,
            'diagnosis': '未知错误',
            'suggestions': ['检查日志'],
            'severity': 'medium'
        }
        
        for error_type, config in AIAnalyzer.ERROR_PATTERNS.items():
            if re.search(config['pattern'], error_message, re.IGNORECASE):
                result['diagnosis'] = config['diagnosis']
                result['suggestions'] = config['suggestions']
                result['error_type'] = error_type
                result['severity'] = 'high' if error_type in ['network'] else 'medium'
                break
        
        return result
    
    @staticmethod
    def batch_analyze(failures: List[Dict]) -> Dict:
        analyses = []
        error_types = {}
        
        for failure in failures:
            analysis = AIAnalyzer.analyze(failure.get('error', ''), failure.get('step', ''))
            analyses.append(analysis)
            error_type = analysis.get('error_type', 'unknown')
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'total_failures': len(failures),
            'analyses': analyses,
            'error_distribution': error_types,
            'top_issue': max(error_types.items(), key=lambda x: x[1])[0] if error_types else 'unknown'
        }

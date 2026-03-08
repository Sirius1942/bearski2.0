import sys
sys.path.insert(0, '/Users/sirius.chen/Documents/projects/BearSki2.0')
from core.ai_analyzer import AIAnalyzer

failures = [
    {'error': 'Timeout waiting for element', 'step': 'login'},
    {'error': 'Element not found: #submit', 'step': 'submit_form'},
    {'error': 'Expected 200 but got 500', 'step': 'api_call'}
]

result = AIAnalyzer.batch_analyze(failures)
print(f"✅ 总失败数: {result['total_failures']}")
print(f"✅ 主要问题: {result['top_issue']}")
print(f"✅ 错误分布: {result['error_distribution']}")

for i, analysis in enumerate(result['analyses'], 1):
    print(f"\n失败 {i} - {analysis['step']}:")
    print(f"  诊断: {analysis['diagnosis']}")
    print(f"  建议: {analysis['suggestions'][0]}")

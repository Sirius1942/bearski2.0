"""测试执行计划生成器测试"""
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.plan_generator import PlanGenerator, ExecutionPlan


# 测试用例数据
test_cases = [
    {'name': 'login_test', 'priority': 'P0', 'tags': ['smoke', 'critical']},
    {'name': 'checkout_test', 'priority': 'P1', 'tags': ['smoke']},
    {'name': 'profile_test', 'priority': 'P2', 'tags': ['ui']},
    {'name': 'search_test', 'priority': 'P3', 'tags': ['feature']}
]

# 1. 按优先级生成计划
print("=== 按优先级生成计划 ===")
priority_plan = PlanGenerator.generate_by_priority(test_cases)
print(f"计划名称: {priority_plan.name}")
print(f"任务数量: {len(priority_plan.tasks)}")
for task in priority_plan.tasks:
    print(f"  - {task['case']} [{task['priority']}]")

# 2. 按标签生成计划
print("\n=== 按标签生成计划 (smoke) ===")
tag_plan = PlanGenerator.generate_by_tags(test_cases, ['smoke'])
print(f"任务数量: {len(tag_plan.tasks)}")
for task in tag_plan.tasks:
    print(f"  - {task['case']} {task['tags']}")

# 3. 定时执行计划
print("\n=== 定时执行计划 ===")
start = datetime.now() + timedelta(hours=1)
scheduled_plan = PlanGenerator.generate_scheduled(test_cases, start, interval_minutes=5)
for task in scheduled_plan.tasks:
    print(f"  - {task['case']} @ {task['scheduled_time'][:16]}")

# 4. 保存和加载
PlanGenerator.save_plan(priority_plan, 'execution_plan.json')
loaded = PlanGenerator.load_plan('execution_plan.json')
print(f"\n✅ 计划已保存并加载: {loaded['name']}")

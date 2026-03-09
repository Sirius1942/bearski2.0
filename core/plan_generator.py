"""测试执行计划生成器"""
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any


class ExecutionPlan:
    """测试执行计划"""
    
    def __init__(self, name: str):
        self.name = name
        self.tasks = []
        self.created_at = datetime.now().isoformat()
    
    def add_task(self, case_name: str, priority: str = 'P2', 
                 scheduled_time: str = None, tags: List[str] = None):
        """添加任务到计划"""
        self.tasks.append({
            'case': case_name,
            'priority': priority,
            'scheduled_time': scheduled_time or datetime.now().isoformat(),
            'tags': tags or [],
            'status': 'pending'
        })
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'created_at': self.created_at,
            'tasks': self.tasks
        }


class PlanGenerator:
    """执行计划生成器"""
    
    @staticmethod
    def generate_by_priority(cases: List[Dict[str, Any]], 
                            priorities: List[str] = None) -> ExecutionPlan:
        """按优先级生成计划"""
        priorities = priorities or ['P0', 'P1', 'P2', 'P3']
        plan = ExecutionPlan('priority_plan')
        
        for priority in priorities:
            for case in cases:
                if case.get('priority') == priority:
                    plan.add_task(case['name'], priority, tags=case.get('tags', []))
        
        return plan
    
    @staticmethod
    def generate_by_tags(cases: List[Dict[str, Any]], 
                        tags: List[str]) -> ExecutionPlan:
        """按标签生成计划"""
        plan = ExecutionPlan('tag_plan')
        
        for case in cases:
            case_tags = case.get('tags', [])
            if any(tag in case_tags for tag in tags):
                plan.add_task(case['name'], case.get('priority', 'P2'), tags=case_tags)
        
        return plan
    
    @staticmethod
    def generate_scheduled(cases: List[Dict[str, Any]], 
                          start_time: datetime,
                          interval_minutes: int = 10) -> ExecutionPlan:
        """生成定时执行计划"""
        plan = ExecutionPlan('scheduled_plan')
        current_time = start_time
        
        for case in cases:
            plan.add_task(
                case['name'],
                case.get('priority', 'P2'),
                current_time.isoformat(),
                case.get('tags', [])
            )
            current_time += timedelta(minutes=interval_minutes)
        
        return plan
    
    @staticmethod
    def save_plan(plan: ExecutionPlan, filepath: str):
        """保存计划到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(plan.to_dict(), f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_plan(filepath: str) -> Dict[str, Any]:
        """从文件加载计划"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

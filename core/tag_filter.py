"""BearSki 2.0 - 测试用例标签过滤器"""
from typing import List, Dict, Set


class TagFilter:
    def __init__(self):
        self.test_cases: Dict[str, Set[str]] = {}
    
    def add_tags(self, test_name: str, tags: List[str]):
        if test_name not in self.test_cases:
            self.test_cases[test_name] = set()
        self.test_cases[test_name].update(tags)
    
    def filter_by_tags(self, tags: List[str], match_all: bool = False) -> List[str]:
        result = []
        tag_set = set(tags)
        for test_name, test_tags in self.test_cases.items():
            if match_all:
                if tag_set.issubset(test_tags):
                    result.append(test_name)
            else:
                if tag_set & test_tags:
                    result.append(test_name)
        return result
    
    def filter_by_expression(self, expr: str) -> List[str]:
        if '!' in expr:
            exclude_tag = expr.replace('!', '').strip()
            return [name for name, tags in self.test_cases.items() 
                   if exclude_tag not in tags]
        if '+' in expr:
            tags = [t.strip() for t in expr.split('+')]
            return self.filter_by_tags(tags, match_all=True)
        if ',' in expr:
            tags = [t.strip() for t in expr.split(',')]
            return self.filter_by_tags(tags, match_all=False)
        return self.filter_by_tags([expr.strip()])

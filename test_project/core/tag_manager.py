"""测试用例标签管理模块"""
import json
from pathlib import Path
from typing import List, Dict, Set

class TagManager:
    """标签管理器"""
    
    def __init__(self, tag_file: str = "tags.json"):
        self.tag_file = Path(tag_file)
        self.tags: Dict[str, Set[str]] = {}
        self._load()
    
    def _load(self):
        """加载标签数据"""
        if self.tag_file.exists():
            with open(self.tag_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tags = {k: set(v) for k, v in data.items()}
    
    def _save(self):
        """保存标签数据"""
        data = {k: list(v) for k, v in self.tags.items()}
        with open(self.tag_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_tag(self, test_name: str, tag: str):
        """为测试用例添加标签"""
        if test_name not in self.tags:
            self.tags[test_name] = set()
        self.tags[test_name].add(tag)
        self._save()
    
    def remove_tag(self, test_name: str, tag: str):
        """移除测试用例标签"""
        if test_name in self.tags:
            self.tags[test_name].discard(tag)
            self._save()
    
    def get_tags(self, test_name: str) -> List[str]:
        """获取测试用例的所有标签"""
        return list(self.tags.get(test_name, set()))
    
    def filter_by_tag(self, tag: str) -> List[str]:
        """根据标签筛选测试用例"""
        return [name for name, tags in self.tags.items() if tag in tags]
    
    def filter_by_tags(self, tags: List[str], match_all: bool = False) -> List[str]:
        """根据多个标签筛选测试用例
        
        Args:
            tags: 标签列表
            match_all: True=匹配所有标签, False=匹配任一标签
        """
        if match_all:
            return [name for name, test_tags in self.tags.items() 
                   if all(tag in test_tags for tag in tags)]
        else:
            return [name for name, test_tags in self.tags.items() 
                   if any(tag in test_tags for tag in tags)]
    
    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        all_tags = set()
        for tags in self.tags.values():
            all_tags.update(tags)
        return sorted(list(all_tags))
    
    def get_tag_stats(self) -> Dict[str, int]:
        """获取标签统计"""
        stats = {}
        for tags in self.tags.values():
            for tag in tags:
                stats[tag] = stats.get(tag, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

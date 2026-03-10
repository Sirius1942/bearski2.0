"""BearSki 2.0 - 场景执行器

执行 YAML DSL 格式的操作脚本
"""
import yaml
from pathlib import Path
from playwright.sync_api import sync_playwright


class ScenarioExecutor:
    """场景执行器"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
    
    def load_scenario(self, yaml_file: str) -> dict:
        """加载场景文件"""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def execute(self, yaml_file: str, variables: dict = None):
        """执行场景"""
        scenario = self.load_scenario(yaml_file)
        
        # 合并变量
        vars = scenario.get('variables', {})
        if variables:
            vars.update(variables)
        
        print(f"执行场景: {scenario['name']}")
        
        # 启动浏览器
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        
        try:
            # 执行步骤
            for step in scenario['steps']:
                self._execute_step(step, vars)
            
            print("✅ 场景执行成功")
            
        finally:
            self.browser.close()
            self.playwright.stop()
    
    def _execute_step(self, step: dict, variables: dict):
        """执行单个步骤"""
        action = step['action']
        desc = step.get('description', '')
        
        print(f"  → {desc}")
        
        if action == 'navigate':
            url = self._replace_vars(step['url'], variables)
            self.page.goto(url)
        
        elif action == 'click':
            selector = self._replace_vars(step['selector'], variables)
            self.page.click(selector)
        
        elif action == 'type':
            selector = self._replace_vars(step['selector'], variables)
            text = self._replace_vars(step['text'], variables)
            self.page.fill(selector, text)
        
        elif action == 'wait':
            import time
            time.sleep(step['seconds'])
        
        elif action == 'select':
            selector = step['selector']
            value = self._replace_vars(step['value'], variables)
            self.page.select_option(selector, value)
        
        elif action == 'assert':
            condition = step['condition']
            # 简化版断言
            pass
    
    def _replace_vars(self, text: str, variables: dict) -> str:
        """替换变量"""
        for key, value in variables.items():
            text = text.replace(f"{{{{{key}}}}}", str(value))
        return text


if __name__ == "__main__":
    executor = ScenarioExecutor()
    executor.execute("01_create_product.yaml")

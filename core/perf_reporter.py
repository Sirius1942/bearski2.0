"""BearSki 2.0 - 性能监控报告"""
import psutil
import time
from typing import Dict


class PerformanceReporter:
    def __init__(self):
        self.samples = []
        self.start_time = None
    
    def start_monitoring(self):
        self.start_time = time.time()
        self.samples = []
    
    def stop_monitoring(self) -> Dict:
        duration = time.time() - self.start_time
        cpu_values = [s['cpu'] for s in self.samples]
        mem_values = [s['memory'] for s in self.samples]
        
        return {
            'duration': duration,
            'avg_cpu': sum(cpu_values) / len(cpu_values) if cpu_values else 0,
            'peak_cpu': max(cpu_values) if cpu_values else 0,
            'avg_memory': sum(mem_values) / len(mem_values) if mem_values else 0,
            'peak_memory': max(mem_values) if mem_values else 0
        }
    
    def sample(self):
        self.samples.append({
            'cpu': psutil.cpu_percent(interval=0.1),
            'memory': psutil.virtual_memory().percent
        })

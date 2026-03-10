"""BearSki 2.0 - 智能重试策略"""
import time
from typing import Callable, Any


class RetryStrategy:
    RETRYABLE_ERRORS = ['timeout', 'network', '503', '502', '504', 'rate limit']
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
    
    def should_retry(self, error: Exception) -> bool:
        error_str = str(error).lower()
        return any(err in error_str for err in self.RETRYABLE_ERRORS)
    
    def calculate_delay(self, attempt: int) -> float:
        return min(2 ** attempt, 32)
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries and self.should_retry(e):
                    delay = self.calculate_delay(attempt)
                    time.sleep(delay)
                    continue
                raise
        raise last_error

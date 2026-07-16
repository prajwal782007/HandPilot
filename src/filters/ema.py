from typing import Tuple
from .base_filter import BaseFilter

class EMAFilter(BaseFilter):
    """
    Exponential Moving Average Filter.
    Simple but effective for constant smoothing.
    """
    def __init__(self, alpha: float = 0.5):
        self.alpha = max(0.0, min(1.0, alpha))
        self.last_value = None

    def __call__(self, value: Tuple[float, float], timestamp: float = -1.0) -> Tuple[float, float]:
        if self.last_value is None:
            self.last_value = value
            return value

        filtered_x = self.alpha * value[0] + (1 - self.alpha) * self.last_value[0]
        filtered_y = self.alpha * value[1] + (1 - self.alpha) * self.last_value[1]
        
        self.last_value = (filtered_x, filtered_y)
        return self.last_value
        
    def reset(self):
        self.last_value = None

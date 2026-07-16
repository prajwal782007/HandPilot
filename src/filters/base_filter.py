from abc import ABC, abstractmethod
from typing import Tuple

class BaseFilter(ABC):
    @abstractmethod
    def __call__(self, value: Tuple[float, float], timestamp: float = -1.0) -> Tuple[float, float]:
        """
        Processes a new point and returns the filtered point.
        """
        pass
    
    @abstractmethod
    def reset(self):
        """
        Resets the filter state.
        """
        pass

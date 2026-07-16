from abc import ABC, abstractmethod
from typing import Optional
from src.models.hand_data import HandData
from src.events.action import Action

class BaseGesture(ABC):
    """
    Abstract base class for a gesture.
    """
    def __init__(self, config_manager=None):
        self.config = config_manager
        
    @abstractmethod
    def detect(self, hand_data: HandData) -> bool:
        """
        Returns True if the gesture is currently being performed.
        """
        pass
        
    @abstractmethod
    def get_action(self) -> Action:
        """
        Returns the action associated with this gesture.
        """
        pass

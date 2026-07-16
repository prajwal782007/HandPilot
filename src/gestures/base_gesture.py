from abc import ABC, abstractmethod
from typing import Optional
from src.models.hand_data import HandData
from src.events.action import Action

class BaseGesture(ABC):
    """
    Abstract base class for a gesture with debounce/stability tracking.
    """
    def __init__(self, config_manager=None):
        self.config = config_manager
        self.active_frames = 0
        self.is_active = False
        
    @abstractmethod
    def detect(self, hand_data: HandData) -> bool:
        """
        Returns True if the physical gesture is currently being performed in this frame.
        """
        pass
        
    def check_stability(self, hand_data: HandData) -> bool:
        """
        Evaluates the gesture, increments active_frames if detected, 
        and returns True only if it meets the debounce threshold.
        """
        detected = self.detect(hand_data)
        debounce_frames = self.config.get_gesture("debounce_frames", 3) if self.config else 3
        
        if detected:
            self.active_frames += 1
            if self.active_frames >= debounce_frames:
                self.is_active = True
                return True
        else:
            self.active_frames = 0
            self.is_active = False
            
        return False
        
    @abstractmethod
    def get_action(self) -> Action:
        """
        Returns the primary action associated with this gesture.
        """
        pass

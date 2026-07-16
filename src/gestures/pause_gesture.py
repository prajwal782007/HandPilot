from src.gestures.base_gesture import BaseGesture
from src.models.hand_data import HandData
from src.events.action import Action
import time

class PauseGesture(BaseGesture):
    def __init__(self, config_manager=None):
        super().__init__(config_manager)
        self.pause_start_time = None
        self.pause_duration = self.config.get_gesture("pause_duration_sec", 1.0) if self.config else 1.0

    def detect(self, hand_data: HandData) -> bool:
        # Pause: Open palm (all fingers extended) held for duration
        all_open = all(hand_data.finger_states.values())
        
        if all_open:
            if self.pause_start_time is None:
                self.pause_start_time = time.time()
            elif time.time() - self.pause_start_time > self.pause_duration:
                return True
        else:
            self.pause_start_time = None
            
        return False

    def get_action(self) -> Action:
        return Action.PAUSE_TRACKING

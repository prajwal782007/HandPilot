from typing import List, Optional
from src.models.hand_data import HandData
from src.gestures.base_gesture import BaseGesture
from src.gestures.click_gestures import LeftClickGesture, RightClickGesture, DoubleClickGesture
from src.gestures.pause_gesture import PauseGesture
from src.events.action import Action
from src.events.event_bus import EventBus
import time

class GestureRecognizer:
    """
    Aggregates all active gestures and processes the current frame's HandData.
    Fires events to the EventBus when gestures are recognized.
    """
    def __init__(self, config_manager=None):
        self.config = config_manager
        self.gestures: List[BaseGesture] = [
            PauseGesture(self.config),
            DoubleClickGesture(self.config), # Check double click before single
            RightClickGesture(self.config),
            LeftClickGesture(self.config)
        ]
        
        self.last_action: Optional[Action] = None
        self.last_action_time = 0.0
        self.cooldown = (self.config.get_gesture("click_cooldown_ms", 300) if self.config else 300) / 1000.0

    def process(self, hand_data: HandData):
        current_time = time.time()
        
        # Debounce/Cooldown logic
        if current_time - self.last_action_time < self.cooldown:
            return
            
        for gesture in self.gestures:
            if gesture.detect(hand_data):
                action = gesture.get_action()
                
                # Emit event
                EventBus.publish(action, payload=hand_data)
                
                self.last_action = action
                self.last_action_time = current_time
                
                # Only trigger one discrete action per frame to avoid conflicts
                break

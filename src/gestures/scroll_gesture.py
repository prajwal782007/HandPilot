from src.gestures.base_gesture import BaseGesture
from src.models.hand_data import HandData
from src.events.action import Action
from src.utils.math_utils import distance
import time

class ScrollGesture(BaseGesture):
    """
    Detects Thumb touching Pinky to enter scroll mode.
    Emits SCROLL_UP or SCROLL_DOWN based on hand movement while active.
    """
    def __init__(self, config_manager=None):
        super().__init__(config_manager)
        self.is_scrolling = False
        self.initial_y = 0.0
        self.last_scroll_time = 0.0
        self.current_action = Action.NONE
        self.scroll_amount = 0

    def detect(self, hand_data: HandData) -> bool:
        threshold = self.config.get_gesture("click_distance", 0.05) if self.config else 0.05
        # Thumb to Pinky
        dist = distance(hand_data.thumb_tip, hand_data.pinky_tip)
        return dist < threshold

    def check_stability(self, hand_data: HandData) -> bool:
        detected = self.detect(hand_data)
        debounce = self.config.get_gesture("debounce_frames", 3) if self.config else 3
        
        # State transitions
        if detected:
            if not self.is_scrolling:
                self.active_frames += 1
                if self.active_frames >= debounce:
                    self.is_scrolling = True
                    self.initial_y = hand_data.palm_center[1]
                    self.active_frames = 0
            else:
                self.active_frames = 0
        else:
            if self.is_scrolling:
                self.active_frames += 1
                if self.active_frames >= debounce:
                    self.is_scrolling = False
                    self.current_action = Action.NONE
                    self.active_frames = 0
                    return False
            else:
                self.active_frames = 0
                
        # If active, evaluate movement
        if self.is_scrolling:
            current_y = hand_data.palm_center[1]
            diff = current_y - self.initial_y
            
            sensitivity = self.config.get_gesture("scroll_sensitivity", 2.0) if self.config else 2.0
            deadzone = 0.05 # Needs to move at least 5% of screen to trigger scroll
            
            # Rate limiting scroll events
            now = time.time()
            if now - self.last_scroll_time > 0.05: # max 20 scrolls per second
                if diff > deadzone:
                    self.current_action = Action.SCROLL_DOWN
                    self.scroll_amount = int(abs(diff - deadzone) * 10 * sensitivity)
                    self.last_scroll_time = now
                    return True
                elif diff < -deadzone:
                    self.current_action = Action.SCROLL_UP
                    self.scroll_amount = int(abs(diff + deadzone) * 10 * sensitivity)
                    self.last_scroll_time = now
                    return True
                    
        self.current_action = Action.NONE
        return False

    def get_action(self) -> Action:
        return self.current_action
        
    def get_payload(self) -> int:
        return max(1, self.scroll_amount)

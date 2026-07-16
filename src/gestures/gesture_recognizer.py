from typing import List, Optional
from src.models.hand_data import HandData
from src.gestures.base_gesture import BaseGesture
from src.gestures.click_gestures import LeftClickGesture, RightClickGesture, DoubleClickGesture
from src.gestures.drag_gesture import DragGesture
from src.gestures.scroll_gesture import ScrollGesture
from src.events.action import Action
from src.events.event_bus import EventBus
import time

class GestureRecognizer:
    """
    Aggregates all active gestures and processes the current frame's HandData.
    Fires events to the EventBus when gestures are recognized.
    Includes state machine and conflict resolution.
    """
    def __init__(self, config_manager=None):
        self.config = config_manager
        
        # Instantiate gestures
        self.double_click = DoubleClickGesture(self.config)
        self.right_click = RightClickGesture(self.config)
        self.left_click = LeftClickGesture(self.config)
        
        self.drag = DragGesture(self.config)
        self.scroll = ScrollGesture(self.config)
        
        self.last_action: Optional[Action] = None
        self.last_action_time = 0.0
        self.cooldown = (self.config.get_gesture("click_cooldown_ms", 250) if self.config else 250) / 1000.0

    def process(self, hand_data: HandData) -> Action:
        current_time = time.time()
        
        # 1. Active State Handlers (Highest Priority once engaged)
        if self.scroll.is_scrolling:
            # If we are already scrolling, only evaluate scroll
            if self.scroll.check_stability(hand_data):
                action = self.scroll.get_action()
                if action != Action.NONE:
                    EventBus.publish(action, payload=self.scroll.get_payload())
                    return action
            return Action.NONE
            
        if self.drag.currently_dragging:
            # If we are dragging, only evaluate drag to see if it ends
            if self.drag.check_stability(hand_data):
                action = self.drag.get_action()
                EventBus.publish(action)
                return action
            return Action.NONE

        # 2. Cooldown check for activation of new discrete actions
        if current_time - self.last_action_time < self.cooldown:
            return Action.NONE
            
        # 3. Activation Priority Check
        # Click gestures have higher priority than scroll/drag activation
        click_gestures = [self.double_click, self.right_click, self.left_click]
        
        for gesture in click_gestures:
            if gesture.check_stability(hand_data):
                action = gesture.get_action()
                EventBus.publish(action)
                self.last_action = action
                self.last_action_time = current_time
                return action
                
        # 4. Drag Activation Check
        if self.drag.check_stability(hand_data):
            action = self.drag.get_action()
            EventBus.publish(action)
            self.last_action = action
            self.last_action_time = current_time
            return action
            
        # 5. Scroll Activation Check
        if self.scroll.check_stability(hand_data):
            # It might have just activated, or immediately triggered a scroll
            action = self.scroll.get_action()
            if action != Action.NONE:
                EventBus.publish(action, payload=self.scroll.get_payload())
                self.last_action = action
                self.last_action_time = current_time
                return action

        return Action.NONE

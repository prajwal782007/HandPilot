from src.gestures.base_gesture import BaseGesture
from src.models.hand_data import HandData
from src.events.action import Action
from src.utils.math_utils import distance

class DragGesture(BaseGesture):
    """
    Detects a closed fist for dragging.
    Returns DRAG_START or DRAG_END based on state.
    """
    def __init__(self, config_manager=None):
        super().__init__(config_manager)
        self.currently_dragging = False

    def detect(self, hand_data: HandData) -> bool:
        threshold = self.config.get_gesture("drag_threshold", 0.05) if self.config else 0.05
        
        # A simple closed fist detection:
        # Check if index, middle, ring, and pinky tips are close to the palm center.
        tips = [
            hand_data.index_tip,
            hand_data.middle_tip,
            hand_data.ring_tip,
            hand_data.pinky_tip
        ]
        
        distances = [distance(tip, hand_data.palm_center) for tip in tips]
        avg_dist = sum(distances) / len(distances)
        
        # We use a slightly looser threshold for the fist distance compared to a precise pinch
        is_fist = avg_dist < (threshold * 3.0) 
        return is_fist

    def check_stability(self, hand_data: HandData) -> bool:
        # Overriding to manage DRAG_START vs DRAG_END state
        detected = self.detect(hand_data)
        debounce = self.config.get_gesture("debounce_frames", 3) if self.config else 3
        
        if detected:
            if not self.currently_dragging:
                self.active_frames += 1
                if self.active_frames >= debounce:
                    self.currently_dragging = True
                    self.active_frames = 0
                    return True # Trigger DRAG_START
            else:
                self.active_frames = 0
        else:
            if self.currently_dragging:
                self.active_frames += 1
                if self.active_frames >= debounce:
                    self.currently_dragging = False
                    self.active_frames = 0
                    return True # Trigger DRAG_END
            else:
                self.active_frames = 0
                
        return False

    def get_action(self) -> Action:
        # If we just became true, it's a START. If we just became false, it's an END.
        return Action.DRAG_START if self.currently_dragging else Action.DRAG_END

from src.gestures.base_gesture import BaseGesture
from src.models.hand_data import HandData
from src.events.action import Action
from src.utils.math_utils import distance

class LeftClickGesture(BaseGesture):
    def detect(self, hand_data: HandData) -> bool:
        threshold = self.config.get_gesture("click_distance", 0.05) if self.config else 0.05
        dist = distance(hand_data.thumb_tip, hand_data.index_tip)
        return dist < threshold

    def get_action(self) -> Action:
        return Action.LEFT_CLICK

class RightClickGesture(BaseGesture):
    def detect(self, hand_data: HandData) -> bool:
        threshold = self.config.get_gesture("click_distance", 0.05) if self.config else 0.05
        dist = distance(hand_data.thumb_tip, hand_data.middle_tip)
        return dist < threshold

    def get_action(self) -> Action:
        return Action.RIGHT_CLICK

class DoubleClickGesture(BaseGesture):
    def detect(self, hand_data: HandData) -> bool:
        threshold = self.config.get_gesture("click_distance", 0.05) if self.config else 0.05
        dist = distance(hand_data.thumb_tip, hand_data.ring_tip)
        return dist < threshold

    def get_action(self) -> Action:
        return Action.DOUBLE_CLICK

import cv2
import time
import math
import mediapipe as mp
from typing import Optional, List
from src.models.hand_data import HandData

class HandTracker:
    """
    Wrapper around MediaPipe Hands to process RGB frames and return standardized HandData.
    """
    def __init__(self, max_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=1 # 0 is faster, 1 is more accurate
        )
        
    def process_frame(self, frame) -> Optional[HandData]:
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        if not results.multi_hand_landmarks:
            return None
            
        # We only care about the first hand if max_hands=1
        hand_landmarks = results.multi_hand_landmarks[0]
        handedness_info = results.multi_handedness[0].classification[0]
        
        # Calculate palm center (average of wrists and MCPs)
        # 0: WRIST, 5: INDEX_FINGER_MCP, 9: MIDDLE_FINGER_MCP, 13: RING_FINGER_MCP, 17: PINKY_MCP
        lm = hand_landmarks.landmark
        
        palm_x = sum([lm[i].x for i in [0, 5, 9, 13, 17]]) / 5
        palm_y = sum([lm[i].y for i in [0, 5, 9, 13, 17]]) / 5
        
        palm_center = (palm_x, palm_y)
        thumb_tip = (lm[4].x, lm[4].y)
        index_tip = (lm[8].x, lm[8].y)
        middle_tip = (lm[12].x, lm[12].y)
        ring_tip = (lm[16].x, lm[16].y)
        pinky_tip = (lm[20].x, lm[20].y)
        
        # Calculate basic finger states based on y-coordinate compared to PIP joint
        # For thumb it's x-coordinate compared based on handedness, but simplified here
        finger_states = {
            "thumb": self._is_thumb_open(lm, handedness_info.label),
            "index": lm[8].y < lm[6].y,
            "middle": lm[12].y < lm[10].y,
            "ring": lm[16].y < lm[14].y,
            "pinky": lm[20].y < lm[18].y
        }
        
        # Rotation calculation (angle between wrist and middle finger MCP)
        dx = lm[9].x - lm[0].x
        dy = lm[9].y - lm[0].y
        rotation = math.degrees(math.atan2(dy, dx))
        
        return HandData(
            palm_center=palm_center,
            thumb_tip=thumb_tip,
            index_tip=index_tip,
            middle_tip=middle_tip,
            ring_tip=ring_tip,
            pinky_tip=pinky_tip,
            handedness=handedness_info.label,
            confidence=handedness_info.score,
            finger_states=finger_states,
            rotation=rotation,
            timestamp=time.time()
        )
        
    def _is_thumb_open(self, lm, handedness_label):
        # MediaPipe flips Left/Right for selfie camera, usually Left means Right hand in image
        if handedness_label == "Right":
            return lm[4].x < lm[3].x
        else:
            return lm[4].x > lm[3].x

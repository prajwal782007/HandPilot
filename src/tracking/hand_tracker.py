import cv2
import time
import mediapipe as mp
from typing import Optional
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
        
        lm = hand_landmarks.landmark
        
        # Extract all 21 landmarks
        all_landmarks = [(l.x, l.y) for l in lm]
        
        # Calculate a stable palm center using wrist (0) and MCP joints (5, 9, 13, 17)
        palm_x = sum([lm[i].x for i in [0, 5, 9, 13, 17]]) / 5
        palm_y = sum([lm[i].y for i in [0, 5, 9, 13, 17]]) / 5
        palm_center = (palm_x, palm_y)
        
        thumb_tip = (lm[4].x, lm[4].y)
        index_tip = (lm[8].x, lm[8].y)
        middle_tip = (lm[12].x, lm[12].y)
        ring_tip = (lm[16].x, lm[16].y)
        pinky_tip = (lm[20].x, lm[20].y)
        
        return HandData(
            landmarks=all_landmarks,
            palm_center=palm_center,
            thumb_tip=thumb_tip,
            index_tip=index_tip,
            middle_tip=middle_tip,
            ring_tip=ring_tip,
            pinky_tip=pinky_tip,
            confidence=handedness_info.score,
            handedness=handedness_info.label,
            timestamp=time.time()
        )

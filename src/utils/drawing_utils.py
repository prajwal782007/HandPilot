import cv2
from src.models.hand_data import HandData

# MediaPipe Hand connections (pairs of landmark indices)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Pinky & Palm base
]

def draw_hand(frame, hand_data: HandData):
    """
    Draws the 21 landmarks, connections, and the stable palm center on the frame.
    """
    if not hand_data:
        return

    h, w, _ = frame.shape
    
    # 1. Draw connections (blue lines)
    for connection in HAND_CONNECTIONS:
        idx1, idx2 = connection
        p1 = hand_data.landmarks[idx1]
        p2 = hand_data.landmarks[idx2]
        
        # Convert normalized coordinates to pixel coordinates
        px1 = int(p1[0] * w)
        py1 = int(p1[1] * h)
        px2 = int(p2[0] * w)
        py2 = int(p2[1] * h)
        
        cv2.line(frame, (px1, py1), (px2, py2), (255, 0, 0), 2)
        
    # 2. Draw 21 landmarks (red dots)
    for landmark in hand_data.landmarks:
        px = int(landmark[0] * w)
        py = int(landmark[1] * h)
        cv2.circle(frame, (px, py), 4, (0, 0, 255), -1)
        
    # 3. Draw palm center (green circle)
    palm_px = int(hand_data.palm_center[0] * w)
    palm_py = int(hand_data.palm_center[1] * h)
    cv2.circle(frame, (palm_px, palm_py), 8, (0, 255, 0), -1)

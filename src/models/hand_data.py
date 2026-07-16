from dataclasses import dataclass
from typing import Dict, Tuple, Optional

@dataclass
class HandData:
    """
    Abstract representation of hand data, decoupled from any specific tracker like MediaPipe.
    All coordinates are normalized [0.0, 1.0].
    """
    palm_center: Tuple[float, float]
    thumb_tip: Tuple[float, float]
    index_tip: Tuple[float, float]
    middle_tip: Tuple[float, float]
    ring_tip: Tuple[float, float]
    pinky_tip: Tuple[float, float]
    
    # "Left" or "Right"
    handedness: str
    
    # Tracker confidence score [0.0, 1.0]
    confidence: float
    
    # State of each finger (True if extended/open, False if folded/closed)
    finger_states: Dict[str, bool]
    
    # Overall rotation angle of the hand (in degrees or radians, depending on implementation)
    rotation: float
    
    # Timestamp of the frame
    timestamp: float

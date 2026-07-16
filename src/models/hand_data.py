from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class HandData:
    """
    Abstract representation of hand data, decoupled from any specific tracker.
    Coordinates are normalized [0.0, 1.0].
    """
    # All 21 landmarks (x, y)
    landmarks: List[Tuple[float, float]]
    
    # Computed stable palm center
    palm_center: Tuple[float, float]
    
    # Specific finger tips for convenience
    thumb_tip: Tuple[float, float]
    index_tip: Tuple[float, float]
    middle_tip: Tuple[float, float]
    ring_tip: Tuple[float, float]
    pinky_tip: Tuple[float, float]
    
    # Tracker confidence score [0.0, 1.0]
    confidence: float
    
    # "Left" or "Right"
    handedness: str
    
    # Timestamp of the frame
    timestamp: float

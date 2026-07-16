from enum import Enum, auto

class Action(Enum):
    # Mouse Actions
    LEFT_CLICK = auto()
    RIGHT_CLICK = auto()
    DOUBLE_CLICK = auto()
    DRAG_START = auto()
    DRAG_END = auto()
    SCROLL_START = auto()
    SCROLL_UP = auto()
    SCROLL_DOWN = auto()
    SCROLL_END = auto()
    
    # System Actions
    PAUSE_TRACKING = auto()
    RESUME_TRACKING = auto()
    
    # Future/Plugin Actions
    VOLUME_UP = auto()
    VOLUME_DOWN = auto()
    VOLUME_MUTE = auto()
    BRIGHTNESS_UP = auto()
    BRIGHTNESS_DOWN = auto()
    OPEN_CHROME = auto()
    OPEN_SPOTIFY = auto()
    
    # Calibration
    CALIBRATE_START = auto()
    CALIBRATE_POINT = auto()
    CALIBRATE_END = auto()

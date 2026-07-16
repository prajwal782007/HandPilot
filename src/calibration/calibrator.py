from typing import Tuple, List, Optional
from src.events.event_bus import EventBus
from src.events.action import Action
import time

class Calibrator:
    """
    Manages the calibration state machine.
    """
    def __init__(self, config_manager=None, display_manager=None):
        self.config = config_manager
        self.display = display_manager
        
        self.is_calibrating = False
        self.points: List[Tuple[float, float]] = []
        # Target: Top Left, Top Right, Bottom Left, Bottom Right
        
    def start_calibration(self):
        self.is_calibrating = True
        self.points = []
        EventBus.publish(Action.CALIBRATE_START)
        
    def register_point(self, norm_x: float, norm_y: float):
        if not self.is_calibrating:
            return
            
        self.points.append((norm_x, norm_y))
        EventBus.publish(Action.CALIBRATE_POINT, payload=len(self.points))
        
        if len(self.points) == 4:
            self.finish_calibration()
            
    def finish_calibration(self):
        self.is_calibrating = False
        
        if len(self.points) == 4:
            # Simple bounds calculation (could be more complex affine transform)
            min_x = min(p[0] for p in self.points)
            max_x = max(p[0] for p in self.points)
            min_y = min(p[1] for p in self.points)
            max_y = max(p[1] for p in self.points)
            
            if self.display:
                self.display.update_calibration((min_x, min_y), (max_x, max_y))
                
            if self.config:
                # Save to config (we need to implement save logic in config_manager for nested items, 
                # or just save to settings.json)
                self.config.settings["calibration"] = {
                    "min_x": min_x, "max_x": max_x,
                    "min_y": min_y, "max_y": max_y
                }
                self.config.save("settings.json", self.config.settings)
                
        EventBus.publish(Action.CALIBRATE_END)

from typing import Tuple, Optional
import win32api

class DisplayManager:
    """
    Manages display info and coordinate mapping.
    Handles multi-monitor setup and calibration mapping.
    """
    def __init__(self):
        self.screen_width = win32api.GetSystemMetrics(0)
        self.screen_height = win32api.GetSystemMetrics(1)
        
        # Calibration bounds (normalized coords [0, 1])
        # Default maps the center 60% of the camera feed to the entire screen
        self.calib_min_x = 0.2
        self.calib_max_x = 0.8
        self.calib_min_y = 0.2
        self.calib_max_y = 0.8

    def update_calibration(self, top_left: Tuple[float, float], bottom_right: Tuple[float, float]):
        self.calib_min_x = top_left[0]
        self.calib_min_y = top_left[1]
        self.calib_max_x = bottom_right[0]
        self.calib_max_y = bottom_right[1]

    def map_to_screen(self, norm_x: float, norm_y: float) -> Tuple[float, float]:
        """
        Maps normalized camera coordinates to absolute screen pixels 
        using the calibration bounds.
        """
        # Map x
        range_x = self.calib_max_x - self.calib_min_x
        if range_x == 0: range_x = 0.001
        screen_x = ((norm_x - self.calib_min_x) / range_x) * self.screen_width
        
        # Map y
        range_y = self.calib_max_y - self.calib_min_y
        if range_y == 0: range_y = 0.001
        screen_y = ((norm_y - self.calib_min_y) / range_y) * self.screen_height
        
        # Clamp to screen bounds
        screen_x = max(0, min(self.screen_width, screen_x))
        screen_y = max(0, min(self.screen_height, screen_y))
        
        return screen_x, screen_y

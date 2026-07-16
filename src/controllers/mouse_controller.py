import time
import math

try:
    from pynput.mouse import Controller as PynputController
    _HAS_PYNPUT = True
except ImportError:
    _HAS_PYNPUT = False

try:
    import pyautogui
    _HAS_PYAUTOGUI = True
except ImportError:
    _HAS_PYAUTOGUI = False

class MouseController:
    """
    Handles OS-level mouse cursor movement based on normalized camera coordinates.
    Hides all OS-specific implementations and dependencies.
    """
    def __init__(self, sensitivity=1.5, smoothing=0.3, dead_zone=2.0, movement_scale=1.2):
        self.sensitivity = sensitivity
        self.smoothing = smoothing
        self.dead_zone = dead_zone
        self.movement_scale = movement_scale
        
        # Screen dimensions
        self.screen_width = 1920
        self.screen_height = 1080
        self._detect_screen_size()
        
        # Internal state
        self.prev_x = 0
        self.prev_y = 0
        self.curr_x = 0
        self.curr_y = 0
        
        self.mouse = None
        if _HAS_PYAUTOGUI:
            pyautogui.FAILSAFE = False # Prevent PyAutoGUI from crashing if cursor hits a corner
            self.backend = "pyautogui"
        elif _HAS_PYNPUT:
            self.mouse = PynputController()
            self.backend = "pynput"
        else:
            self.backend = "none"
            print("WARNING: Neither pynput nor pyautogui is installed. Mouse movement will not work.")

    def _detect_screen_size(self):
        """Automatically detect screen resolution"""
        if _HAS_PYAUTOGUI:
            size = pyautogui.size()
            self.screen_width = size.width
            self.screen_height = size.height
        else:
            # Fallback for Windows using ctypes
            try:
                import ctypes
                user32 = ctypes.windll.user32
                self.screen_width = user32.GetSystemMetrics(0)
                self.screen_height = user32.GetSystemMetrics(1)
            except Exception:
                print("WARNING: Could not detect screen size. Defaulting to 1920x1080.")

    def _map_to_screen(self, normalized_x, normalized_y):
        """
        Maps normalized camera coordinates [0, 1] to screen coordinates.
        Uses movement_scale to create an inner box so users can easily reach edges.
        """
        # Center the coordinates around 0.5
        centered_x = normalized_x - 0.5
        centered_y = normalized_y - 0.5
        
        # Apply scaling
        scaled_x = centered_x * self.movement_scale * self.sensitivity
        scaled_y = centered_y * self.movement_scale * self.sensitivity
        
        # Move back to [0, 1] space
        mapped_x = scaled_x + 0.5
        mapped_y = scaled_y + 0.5
        
        # Convert to screen pixels
        screen_x = int(mapped_x * self.screen_width)
        screen_y = int(mapped_y * self.screen_height)
        
        # Clamp to screen boundaries
        screen_x = max(0, min(self.screen_width - 1, screen_x))
        screen_y = max(0, min(self.screen_height - 1, screen_y))
        
        return screen_x, screen_y

    def _apply_smoothing(self, target_x, target_y):
        """Applies exponential smoothing to the movement."""
        if self.prev_x == 0 and self.prev_y == 0:
            self.curr_x = target_x
            self.curr_y = target_y
        else:
            self.curr_x = self.prev_x + (target_x - self.prev_x) * self.smoothing
            self.curr_y = self.prev_y + (target_y - self.prev_y) * self.smoothing
            
        return int(self.curr_x), int(self.curr_y)

    def _check_dead_zone(self, x, y):
        """Returns True if the movement is larger than the dead zone threshold."""
        distance = math.sqrt((x - self.prev_x)**2 + (y - self.prev_y)**2)
        return distance > self.dead_zone

    def move_cursor(self, normalized_x, normalized_y):
        """
        Moves the mouse cursor to the mapped position of the given normalized camera coordinates.
        Returns the final calculated (screen_x, screen_y) for debugging purposes.
        """
        target_x, target_y = self._map_to_screen(normalized_x, normalized_y)
        smoothed_x, smoothed_y = self._apply_smoothing(target_x, target_y)
        
        print(f"Logging: MouseController called with Palm coords: X:{normalized_x:.3f}, Y:{normalized_y:.3f}")
        print(f"Logging: Mapped screen coordinates: X:{smoothed_x}, Y:{smoothed_y}")
        
        if self._check_dead_zone(smoothed_x, smoothed_y):
            self._execute_move(smoothed_x, smoothed_y)
            self.prev_x = smoothed_x
            self.prev_y = smoothed_y
            return smoothed_x, smoothed_y
            
        return int(self.prev_x), int(self.prev_y)
        
    def _execute_move(self, x, y):
        """Internal method to execute the OS-level move."""
        print(f"Logging: Moving cursor to: X: {x}, Y: {y} using backend: {self.backend}")
        
        success = False
        if self.backend == "pynput" and self.mouse:
            try:
                self.mouse.position = (x, y)
                success = True
            except Exception as e:
                print(f"ERROR: pynput failed to move cursor: {e}")
                success = False
                
        if not success and _HAS_PYAUTOGUI:
            # Fallback to pyautogui
            if self.backend == "pynput":
                print("WARNING: Automatically falling back to PyAutoGUI...")
                self.backend = "pyautogui"
            try:
                pyautogui.moveTo(x, y, _pause=False)
                success = True
            except Exception as e:
                print(f"ERROR: pyautogui failed to move cursor: {e}")
                
        if success:
            print("Logging: OS cursor updated")

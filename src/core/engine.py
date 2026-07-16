import threading
import time
from src.camera.capture_thread import CaptureThread
from src.tracking.hand_tracker import HandTracker
from src.gestures.gesture_recognizer import GestureRecognizer
from src.controllers.display_manager import DisplayManager
from src.controllers.mouse_controller import MouseController
from src.core.action_manager import ActionManager
from src.filters.one_euro import OneEuroFilter
from src.calibration.calibrator import Calibrator

class Engine:
    """
    Central orchestrator tying all modules together.
    Runs the main processing loop.
    """
    def __init__(self, config_manager, ui_overlay=None):
        self.config = config_manager
        self.ui = ui_overlay
        
        self.display = DisplayManager()
        self.mouse = MouseController()
        self.action_manager = ActionManager(self.mouse, None)
        self.calibrator = Calibrator(self.config, self.display)
        
        self.capture_thread = CaptureThread(
            camera_index=self.config.get_camera("camera_index", 0),
            width=self.config.get_camera("resolution_width", 1280),
            height=self.config.get_camera("resolution_height", 720),
            target_fps=self.config.get_camera("target_fps", 60)
        )
        
        self.tracker = HandTracker()
        self.recognizer = GestureRecognizer(self.config)
        
        # Load filter (using OneEuro default)
        self.filter = OneEuroFilter(t0=time.time(), x0=(0.0, 0.0))
        
        self.running = False
        self.thread = None
        self.current_fps = 0.0
        self.is_paused = False

    def start(self):
        self.capture_thread.start()
        self.running = True
        self.thread = threading.Thread(target=self._process_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.capture_thread.stop()

    def _process_loop(self):
        last_time = time.time()
        frames_count = 0
        fps_update_time = time.time()
        
        while self.running:
            frame = self.capture_thread.get_frame()
            if frame is None:
                time.sleep(0.005)
                continue
                
            hand_data = self.tracker.process_frame(frame)
            
            if hand_data:
                # Process gestures
                self.recognizer.process(hand_data)
                
                # Check for pause state
                if self.recognizer.last_action and self.recognizer.last_action.name == "PAUSE_TRACKING":
                    self.is_paused = not self.is_paused
                    # Reset action so it doesn't toggle repeatedly
                    self.recognizer.last_action = None
                    self.filter.reset()
                
                # If active, process cursor movement
                if not self.is_paused and not self.calibrator.is_calibrating:
                    # Apply filter
                    smoothed = self.filter(hand_data.palm_center, hand_data.timestamp)
                    
                    # Map to screen
                    screen_x, screen_y = self.display.map_to_screen(smoothed[0], smoothed[1])
                    
                    # Move mouse
                    self.mouse.move(screen_x, screen_y)
                    
                # If calibrating
                if self.calibrator.is_calibrating and self.recognizer.last_action and self.recognizer.last_action.name == "LEFT_CLICK":
                    self.calibrator.register_point(hand_data.palm_center[0], hand_data.palm_center[1])
                    self.recognizer.last_action = None

            # Calculate FPS
            frames_count += 1
            if time.time() - fps_update_time >= 1.0:
                self.current_fps = frames_count / (time.time() - fps_update_time)
                frames_count = 0
                fps_update_time = time.time()
                
            # Update UI
            if self.ui and hand_data:
                gesture_name = self.recognizer.last_action.name if self.recognizer.last_action else "None"
                # The UI update must be thread-safe in PyQt6. We'll use a signal or QTimer 
                # in the real app, but for this simplified version, QTimer in UI is better.
                # Just store the values.
                self.ui.current_fps = self.current_fps
                self.ui.current_gesture = gesture_name
                self.ui.is_paused = self.is_paused

import sys
import os
import cv2
import time
import json
import numpy as np

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.camera.video_capture import Camera
from src.tracking.hand_tracker import HandTracker
from src.utils.drawing_utils import draw_hand
from src.controllers.mouse_controller import MouseController

def load_settings(config_path="config/settings.json"):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"WARNING: Failed to load settings.json: {e}")
        return {}

def show_error_screen(message):
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    cv2.putText(frame, "CAMERA ERROR", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
    cv2.putText(frame, message, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Press 'q' to exit", (50, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
    while True:
        cv2.imshow("HandPilot Milestone 2", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def main():
    print("Initializing HandPilot Milestone 2 - Smooth Mouse Control")
    
    settings = load_settings()
    sensitivity = settings.get("cursor_sensitivity", 1.5)
    smoothing = settings.get("smoothing_factor", 0.3)
    dead_zone = settings.get("dead_zone", 2.0)
    movement_scale = settings.get("movement_scale", 1.2)
    
    # Initialize Camera
    camera = Camera(camera_index=None, width=1280, height=720, target_fps=60)
    if not camera.start():
        print("Failed to open webcam.")
        show_error_screen("Failed to initialize webcam on any index/backend.")
        sys.exit(1)
        
    # Initialize Tracker and Controller
    tracker = HandTracker()
    mouse_controller = MouseController(
        sensitivity=sensitivity,
        smoothing=smoothing,
        dead_zone=dead_zone,
        movement_scale=movement_scale
    )
    
    mouse_enabled = False
    prev_time = time.time()
    
    try:
        while True:
            ret, frame = camera.read_frame()
            if not ret or frame is None:
                continue
                
            # Process frame
            hand_data = tracker.process_frame(frame)
            
            screen_x, screen_y = 0, 0
            palm_x, palm_y = 0.0, 0.0
            
            if hand_data:
                draw_hand(frame, hand_data)
                
                palm_x, palm_y = hand_data.palm_center
                
                # Mirror X-axis so that moving hand right moves cursor right
                mirrored_x = 1.0 - palm_x 
                
                if mouse_enabled:
                    screen_x, screen_y = mouse_controller.move_cursor(mirrored_x, palm_y)
                else:
                    # Still calculate mapping for debug overlay even if disabled
                    screen_x, screen_y = mouse_controller._map_to_screen(mirrored_x, palm_y)

            # Calculate FPS
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time
            
            # --- Debug Overlay ---
            overlay_text = [
                f"FPS: {int(fps)}",
                f"Status: {'ENABLED' if mouse_enabled else 'DISABLED'} (Press 'm' to toggle, ESC to stop)",
                f"Palm X: {palm_x:.3f} Y: {palm_y:.3f}",
                f"Screen X: {screen_x} Y: {screen_y}"
            ]
            
            y_offset = 30
            for i, text in enumerate(overlay_text):
                color = (0, 255, 0) if mouse_enabled else (0, 165, 255)
                if i == 1 and not mouse_enabled: color = (0, 0, 255)
                cv2.putText(frame, text, (20, y_offset + (i * 30)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Show Window
            cv2.imshow("HandPilot Milestone 2", frame)
            
            # Keyboard Events
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('m'):
                mouse_enabled = not mouse_enabled
            elif key == 27: # ESC
                mouse_enabled = False
                
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        print("Cleaning up...")
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

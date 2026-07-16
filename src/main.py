import sys
import os
import cv2
import time
import numpy as np

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.camera.video_capture import Camera
from src.tracking.hand_tracker import HandTracker
from src.utils.drawing_utils import draw_hand
from src.controllers.mouse_controller import MouseController
from src.config.config_manager import ConfigManager
from src.core.action_manager import ActionManager
from src.gestures.gesture_recognizer import GestureRecognizer
from src.events.action import Action
from src.utils.math_utils import distance

def show_error_screen(message):
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    cv2.putText(frame, "CAMERA ERROR", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
    cv2.putText(frame, message, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Press 'q' to exit", (50, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
    while True:
        cv2.imshow("HandPilot Milestone 3", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def main():
    print("Initializing HandPilot Milestone 3 - Gesture Engine")
    
    config = ConfigManager()
    
    settings = config.settings
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
        
    # Initialize Core Components
    tracker = HandTracker()
    mouse_controller = MouseController(
        sensitivity=sensitivity,
        smoothing=smoothing,
        dead_zone=dead_zone,
        movement_scale=movement_scale
    )
    
    action_manager = ActionManager(mouse_controller)
    gesture_recognizer = GestureRecognizer(config)
    
    mouse_enabled = False
    debug_mode = False
    
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
            
            current_action = Action.NONE
            
            if hand_data:
                draw_hand(frame, hand_data)
                
                palm_x, palm_y = hand_data.palm_center
                mirrored_x = 1.0 - palm_x 
                
                # 1. Evaluate Gestures (Independent of Mouse Enabled state, but actions route through ActionManager)
                current_action = gesture_recognizer.process(hand_data)
                
                # 2. Evaluate Mouse Movement
                if mouse_enabled:
                    screen_x, screen_y = mouse_controller.move_cursor(mirrored_x, palm_y)
                else:
                    # Still calculate mapping for debug overlay
                    screen_x, screen_y = mouse_controller._map_to_screen(mirrored_x, palm_y)

            # Calculate FPS
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time
            
            # --- Standard Overlay ---
            overlay_text = [
                f"FPS: {int(fps)}",
                f"Status: {'ENABLED' if mouse_enabled else 'DISABLED'} (M: Toggle, ESC: Stop)",
                f"Test Mode: {'ON' if action_manager.test_mode else 'OFF'} (T: Toggle)",
                f"Action: {current_action.name if current_action != Action.NONE else 'NONE'}"
            ]
            
            y_offset = 30
            for i, text in enumerate(overlay_text):
                color = (0, 255, 0) if mouse_enabled else (0, 165, 255)
                if i == 1 and not mouse_enabled: color = (0, 0, 255)
                if i == 2 and action_manager.test_mode: color = (0, 255, 255)
                cv2.putText(frame, text, (20, y_offset + (i * 30)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                            
            # --- Debug Overlay ---
            if debug_mode and hand_data:
                debug_y_offset = y_offset + (len(overlay_text) * 30) + 20
                
                dist_li = distance(hand_data.thumb_tip, hand_data.index_tip)
                dist_lm = distance(hand_data.thumb_tip, hand_data.middle_tip)
                dist_lr = distance(hand_data.thumb_tip, hand_data.ring_tip)
                dist_lp = distance(hand_data.thumb_tip, hand_data.pinky_tip)
                
                cooldown_remaining = max(0, gesture_recognizer.cooldown - (curr_time - gesture_recognizer.last_action_time))
                
                debug_text = [
                    f"--- DEBUG (D to Hide) ---",
                    f"Thumb-Index (Left Click): {dist_li:.3f}",
                    f"Thumb-Mid (Right Click): {dist_lm:.3f}",
                    f"Thumb-Ring (Double Click): {dist_lr:.3f}",
                    f"Thumb-Pinky (Scroll): {dist_lp:.3f}",
                    f"Is Dragging: {gesture_recognizer.drag.currently_dragging}",
                    f"Is Scrolling: {gesture_recognizer.scroll.is_scrolling}",
                    f"Cooldown: {cooldown_remaining:.2f}s"
                ]
                
                for i, text in enumerate(debug_text):
                    cv2.putText(frame, text, (20, debug_y_offset + (i * 25)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            # Show Window
            cv2.imshow("HandPilot Milestone 3", frame)
            
            # Keyboard Events
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('m'):
                mouse_enabled = not mouse_enabled
            elif key == ord('t'):
                action_manager.set_test_mode(not action_manager.test_mode)
            elif key == ord('d'):
                debug_mode = not debug_mode
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

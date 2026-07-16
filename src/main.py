import sys
import os
import cv2
import time

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.camera.video_capture import Camera
from src.tracking.hand_tracker import HandTracker
from src.utils.drawing_utils import draw_hand

def main():
    print("Initializing HandPilot Milestone 1 - Tracking Foundation")
    
    # Initialize Camera
    camera = Camera(camera_index=0, width=1280, height=720, target_fps=60)
    if not camera.start():
        print("Failed to open webcam.")
        sys.exit(1)
        
    # Initialize Tracker
    tracker = HandTracker()
    
    # Variables for FPS calculation
    prev_time = time.time()
    
    try:
        while True:
            ret, frame = camera.read_frame()
            if not ret or frame is None:
                continue
                
            # Process frame
            hand_data = tracker.process_frame(frame)
            
            # Draw landmarks and palm center
            if hand_data:
                draw_hand(frame, hand_data)
                
            # Calculate FPS
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time
            
            # Draw FPS
            cv2.putText(frame, f"FPS: {int(fps)}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
            # Show Window
            cv2.imshow("HandPilot Tracking Foundation", frame)
            
            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        print("Cleaning up...")
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

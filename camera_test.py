import cv2
import time

def test_cameras():
    print("Starting Camera Diagnostics...")
    backends = [
        (cv2.CAP_MSMF, "CAP_MSMF"),
        (cv2.CAP_DSHOW, "CAP_DSHOW"),
        (None, "Default")
    ]
    
    working_cam = None
    working_backend = None
    working_index = -1
    
    for index in range(6):
        for backend_flag, backend_name in backends:
            print(f"Testing camera index {index} with backend {backend_name}...")
            cap = cv2.VideoCapture(index, backend_flag) if backend_flag is not None else cv2.VideoCapture(index)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None and frame.size > 0:
                    print(f"  -> SUCCESS! Camera found at index {index} with {backend_name}")
                    working_cam = cap
                    working_backend = backend_name
                    working_index = index
                    break
                else:
                    print("  -> Opened, but failed to read frame.")
                    cap.release()
            else:
                print("  -> Failed to open.")
        
        if working_cam is not None:
            break
            
    if working_cam is None:
        print("No working camera found.")
        return
        
    print(f"\n--- Diagnostic Info ---")
    print(f"Camera Index: {working_index}")
    print(f"Backend: {working_backend}")
    
    width = int(working_cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(working_cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Resolution: {width}x{height}")
    
    prev_time = time.time()
    
    try:
        while True:
            ret, frame = working_cam.read()
            if not ret or frame is None:
                print("Lost connection to camera!")
                break
                
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time
            
            cv2.putText(frame, f"Backend: {working_backend} Index: {working_index}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Res: {width}x{height}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"FPS: {int(fps)}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Camera Diagnostic Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        working_cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test_cameras()

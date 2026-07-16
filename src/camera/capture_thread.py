import cv2
import threading
import time
import queue

class CaptureThread(threading.Thread):
    """
    Dedicated thread for reading frames from the webcam to avoid blocking the main processing loop.
    """
    def __init__(self, camera_index=0, width=1280, height=720, target_fps=60):
        super().__init__()
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.target_fps = target_fps
        self.frame_queue = queue.Queue(maxsize=2)
        
        self.running = False
        self.cap = None

    def run(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.target_fps)

        self.running = True
        
        # We try to maintain the target FPS reading
        frame_time = 1.0 / self.target_fps
        
        while self.running:
            start_time = time.time()
            
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
                
            # If the queue is full, remove the oldest frame to avoid latency
            if self.frame_queue.full():
                try:
                    self.frame_queue.get_nowait()
                except queue.Empty:
                    pass
                    
            self.frame_queue.put(frame)
            
            elapsed = time.time() - start_time
            sleep_time = max(0, frame_time - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)

        if self.cap:
            self.cap.release()

    def get_frame(self):
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        self.running = False
        self.join()

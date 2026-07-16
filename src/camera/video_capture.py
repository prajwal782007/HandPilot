import cv2

class Camera:
    """
    Robust camera class responsible for opening webcam, reading frames, and cleaning up.
    """
    def __init__(self, camera_index=None, width=1280, height=720, target_fps=60):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.target_fps = target_fps
        self.cap = None
        self.backend_name = "Unknown"

    def _try_open_camera(self, index, backend_flag, backend_name):
        if backend_flag is None:
            cap = cv2.VideoCapture(index)
        else:
            cap = cv2.VideoCapture(index, backend_flag)
            
        if cap.isOpened():
            # Set properties before reading to prevent MSMF backend crash
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            cap.set(cv2.CAP_PROP_FPS, self.target_fps)
            
            # Check if it actually reads a frame
            ret, frame = cap.read()
            if ret and frame is not None and frame.size > 0:
                print(f"DEBUG: Camera opened on index {index} with backend {backend_name}")
                print(f"DEBUG: Frame resolution: {frame.shape[1]}x{frame.shape[0]}")
                print(f"DEBUG: Frames are being received: Yes")
                return cap
            else:
                cap.release()
        return None

    def start(self) -> bool:
        """Initializes the webcam and sets properties."""
        backends = [
            (cv2.CAP_MSMF, "CAP_MSMF"),
            (cv2.CAP_DSHOW, "CAP_DSHOW"),
            (None, "Default")
        ]
        
        indices_to_try = [self.camera_index] if self.camera_index is not None else range(6)
        
        for index in indices_to_try:
            for backend_flag, backend_name in backends:
                print(f"DEBUG: Trying camera index {index} with backend {backend_name}...")
                cap = self._try_open_camera(index, backend_flag, backend_name)
                if cap is not None:
                    self.cap = cap
                    self.camera_index = index
                    self.backend_name = backend_name
                    print(f"Logging: Camera opened")
                    return True
                    
        print("DEBUG: Failed to find a working camera backend and index combination.")
        return False

    def read_frame(self):
        """Reads a frame from the webcam. Returns (success, frame)."""
        if self.cap is None or not self.cap.isOpened():
            print("ERROR: cap is None or not opened when reading frame.")
            return False, None
            
        ret, frame = self.cap.read()
        if not ret:
            print("ERROR: cap.read() returned False. Failed to receive frame.")
            return False, None
            
        if frame is None or frame.size == 0:
            print("ERROR: cap.read() returned empty or None frame.")
            return False, None
            
        return ret, frame

    def release(self):
        """Releases the webcam resources properly."""
        if self.cap:
            self.cap.release()
            self.cap = None

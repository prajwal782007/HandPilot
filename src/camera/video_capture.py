import cv2

class Camera:
    """
    Robust camera class responsible for opening webcam, reading frames, and cleaning up.
    """
    def __init__(self, camera_index=0, width=1280, height=720, target_fps=60):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.target_fps = target_fps
        self.cap = None

    def start(self) -> bool:
        """Initializes the webcam and sets properties."""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            return False
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.target_fps)
        return True

    def read_frame(self):
        """Reads a frame from the webcam. Returns (success, frame)."""
        if self.cap is None or not self.cap.isOpened():
            return False, None
            
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        """Releases the webcam resources properly."""
        if self.cap:
            self.cap.release()
            self.cap = None

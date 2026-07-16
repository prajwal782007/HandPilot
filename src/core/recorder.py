class Recorder:
    """
    Records sequences of gestures and mouse movements into macros.
    """
    def __init__(self):
        self.is_recording = False
        self.macro = []
        
    def start_recording(self):
        self.is_recording = True
        self.macro = []
        
    def stop_recording(self):
        self.is_recording = False
        
    def add_event(self, event_type, payload):
        if self.is_recording:
            self.macro.append((event_type, payload))
            
    def save_macro(self, name):
        pass

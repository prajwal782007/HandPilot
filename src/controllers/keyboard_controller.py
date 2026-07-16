import pynput.keyboard as pkeyboard

class KeyboardController:
    """
    OS-level keyboard interactions using pynput.
    """
    def __init__(self):
        self.keyboard = pkeyboard.Controller()

    def press(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)
        
    def type_string(self, text):
        self.keyboard.type(text)

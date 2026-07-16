import pynput.mouse as pmouse
import time

class MouseController:
    """
    OS-level mouse interactions using pynput for low latency.
    """
    def __init__(self):
        self.mouse = pmouse.Controller()
        self.is_dragging = False

    def move(self, x: float, y: float):
        """Moves the mouse to the absolute screen coordinates."""
        self.mouse.position = (x, y)

    def left_click(self):
        self.mouse.click(pmouse.Button.left, 1)

    def right_click(self):
        self.mouse.click(pmouse.Button.right, 1)

    def double_click(self):
        self.mouse.click(pmouse.Button.left, 2)

    def drag_start(self):
        if not self.is_dragging:
            self.mouse.press(pmouse.Button.left)
            self.is_dragging = True

    def drag_end(self):
        if self.is_dragging:
            self.mouse.release(pmouse.Button.left)
            self.is_dragging = False

    def scroll_up(self, amount=1):
        self.mouse.scroll(0, amount)

    def scroll_down(self, amount=1):
        self.mouse.scroll(0, -amount)

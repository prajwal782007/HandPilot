import time
from src.events.action import Action
from src.events.event_bus import EventBus
from src.controllers.mouse_controller import MouseController

class ActionManager:
    """
    Decouples gesture recognition from OS execution.
    Listens to the EventBus and routes actions to the MouseController.
    Respects the 'test_mode' flag to prevent actual OS clicks when debugging.
    """
    def __init__(self, mouse_controller: MouseController):
        self.mouse = mouse_controller
        self.test_mode = False
        
        self._setup_subscriptions()
        
    def _setup_subscriptions(self):
        EventBus.subscribe(Action.LEFT_CLICK, self._on_left_click)
        EventBus.subscribe(Action.RIGHT_CLICK, self._on_right_click)
        EventBus.subscribe(Action.DOUBLE_CLICK, self._on_double_click)
        EventBus.subscribe(Action.DRAG_START, self._on_drag_start)
        EventBus.subscribe(Action.DRAG_END, self._on_drag_end)
        EventBus.subscribe(Action.SCROLL_UP, self._on_scroll_up)
        EventBus.subscribe(Action.SCROLL_DOWN, self._on_scroll_down)
        
    def set_test_mode(self, enabled: bool):
        self.test_mode = enabled
        if self.test_mode:
            print("[ActionManager] Test Mode ENABLED (OS Actions disabled)")
        else:
            print("[ActionManager] Test Mode DISABLED (OS Actions live)")

    def _on_left_click(self, payload):
        if self.test_mode:
            print("[TEST MODE] Action: LEFT_CLICK")
            return
        if self.mouse:
            self.mouse.left_click()

    def _on_right_click(self, payload):
        if self.test_mode:
            print("[TEST MODE] Action: RIGHT_CLICK")
            return
        if self.mouse:
            self.mouse.right_click()

    def _on_double_click(self, payload):
        if self.test_mode:
            print("[TEST MODE] Action: DOUBLE_CLICK")
            return
        if self.mouse:
            self.mouse.double_click()

    def _on_drag_start(self, payload):
        if self.test_mode:
            print("[TEST MODE] Action: DRAG_START")
            return
        if self.mouse:
            self.mouse.drag_start()

    def _on_drag_end(self, payload):
        if self.test_mode:
            print("[TEST MODE] Action: DRAG_END")
            return
        if self.mouse:
            self.mouse.drag_end()

    def _on_scroll_up(self, payload):
        amount = payload if isinstance(payload, int) else 1
        if self.test_mode:
            print(f"[TEST MODE] Action: SCROLL_UP ({amount})")
            return
        if self.mouse:
            self.mouse.scroll(1, amount)

    def _on_scroll_down(self, payload):
        amount = payload if isinstance(payload, int) else 1
        if self.test_mode:
            print(f"[TEST MODE] Action: SCROLL_DOWN ({amount})")
            return
        if self.mouse:
            self.mouse.scroll(-1, amount)

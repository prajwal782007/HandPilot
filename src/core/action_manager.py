from src.events.action import Action
from src.events.event_bus import EventBus
# from src.controllers.mouse_controller import MouseController
# from src.controllers.keyboard_controller import KeyboardController

class ActionManager:
    """
    Listens to the EventBus and routes actions to the appropriate controllers.
    """
    def __init__(self, mouse_controller=None, keyboard_controller=None):
        self.mouse = mouse_controller
        self.keyboard = keyboard_controller
        
        self._setup_subscriptions()
        
    def _setup_subscriptions(self):
        EventBus.subscribe(Action.LEFT_CLICK, self._on_left_click)
        EventBus.subscribe(Action.RIGHT_CLICK, self._on_right_click)
        EventBus.subscribe(Action.DOUBLE_CLICK, self._on_double_click)
        EventBus.subscribe(Action.DRAG_START, self._on_drag_start)
        EventBus.subscribe(Action.DRAG_END, self._on_drag_end)
        EventBus.subscribe(Action.SCROLL_UP, self._on_scroll_up)
        EventBus.subscribe(Action.SCROLL_DOWN, self._on_scroll_down)
        
    def _on_left_click(self, payload):
        if self.mouse:
            self.mouse.left_click()
            
    def _on_right_click(self, payload):
        if self.mouse:
            self.mouse.right_click()
            
    def _on_double_click(self, payload):
        if self.mouse:
            self.mouse.double_click()
            
    def _on_drag_start(self, payload):
        if self.mouse:
            self.mouse.drag_start()
            
    def _on_drag_end(self, payload):
        if self.mouse:
            self.mouse.drag_end()
            
    def _on_scroll_up(self, payload):
        if self.mouse:
            self.mouse.scroll_up()
            
    def _on_scroll_down(self, payload):
        if self.mouse:
            self.mouse.scroll_down()

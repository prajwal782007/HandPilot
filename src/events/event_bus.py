from typing import Callable, Dict, List, Any
from .action import Action
import threading

class EventBus:
    """
    Central event bus for publisher-subscriber communication.
    Allows decoupling gesture recognition from action execution.
    """
    _subscribers: Dict[Action, List[Callable[[Any], None]]] = {}
    _lock = threading.Lock()
    
    @classmethod
    def subscribe(cls, action: Action, callback: Callable[[Any], None]):
        with cls._lock:
            if action not in cls._subscribers:
                cls._subscribers[action] = []
            if callback not in cls._subscribers[action]:
                cls._subscribers[action].append(callback)
                
    @classmethod
    def unsubscribe(cls, action: Action, callback: Callable[[Any], None]):
        with cls._lock:
            if action in cls._subscribers and callback in cls._subscribers[action]:
                cls._subscribers[action].remove(callback)
                
    @classmethod
    def publish(cls, action: Action, payload: Any = None):
        """
        Publishes an action to all subscribers.
        This runs in the same thread as the publisher. For long running tasks, 
        the subscriber should handle threading.
        """
        with cls._lock:
            subs = list(cls._subscribers.get(action, []))
            
        for callback in subs:
            try:
                callback(payload)
            except Exception as e:
                # In a real app we'd log this
                print(f"Error in EventBus subscriber for {action}: {e}")

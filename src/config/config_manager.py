import json
import os
from typing import Dict, Any

class ConfigManager:
    """
    Manages loading and saving JSON configuration files.
    """
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.settings = self._load("settings.json")
        self.camera = self._load("camera.json")
        self.gestures = self._load("gestures.json")
        self.ui = self._load("ui.json")

    def _load(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.config_dir, filename)
        if not os.path.exists(filepath):
            return {}
        with open(filepath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save(self, filename: str, data: Dict[str, Any]):
        filepath = os.path.join(self.config_dir, filename)
        os.makedirs(self.config_dir, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
    def get_setting(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)
        
    def get_camera(self, key: str, default: Any = None) -> Any:
        return self.camera.get(key, default)
        
    def get_gesture(self, key: str, default: Any = None) -> Any:
        return self.gestures.get(key, default)
        
    def get_ui(self, key: str, default: Any = None) -> Any:
        return self.ui.get(key, default)

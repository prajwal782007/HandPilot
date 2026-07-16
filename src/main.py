import sys
import os
# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.config.config_manager import ConfigManager
from src.ui.overlay import Overlay
from src.core.engine import Engine

def main():
    app = QApplication(sys.argv)
    
    config = ConfigManager("config")
    
    overlay = Overlay(config)
    
    # Store attributes for thread-safe UI updates
    overlay.current_fps = 0.0
    overlay.current_gesture = "None"
    overlay.is_paused = False
    
    engine = Engine(config, overlay)
    
    # Use QTimer to update UI safely from the main thread
    timer = QTimer()
    timer.timeout.connect(lambda: overlay.update_info(
        overlay.current_fps, 
        overlay.current_gesture, 
        overlay.is_paused
    ))
    timer.start(100) # 10fps UI update is enough
    
    # Start engine in background
    engine.start()
    overlay.show()
    
    # Execute App
    exit_code = app.exec()
    
    # Clean up
    engine.stop()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

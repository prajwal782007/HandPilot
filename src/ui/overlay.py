from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
import sys

class Overlay(QWidget):
    """
    Transparent floating control panel.
    Displays current status, FPS, and recognized gesture.
    """
    def __init__(self, config_manager=None):
        super().__init__()
        self.config = config_manager
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # UI Styling from config
        opacity = self.config.get_ui("opacity", 0.8) if self.config else 0.8
        bg_color = f"rgba(30, 30, 30, {int(opacity * 255)})"
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        font_title = QFont("Segoe UI", 12, QFont.Weight.Bold)
        font_body = QFont("Segoe UI", 10)
        
        self.title = QLabel("HandPilot")
        self.title.setFont(font_title)
        
        self.lbl_fps = QLabel("FPS: --")
        self.lbl_fps.setFont(font_body)
        
        self.lbl_gesture = QLabel("Gesture: None")
        self.lbl_gesture.setFont(font_body)
        
        self.lbl_status = QLabel("Status: Active")
        self.lbl_status.setFont(font_body)
        
        layout.addWidget(self.title)
        layout.addWidget(self.lbl_fps)
        layout.addWidget(self.lbl_gesture)
        layout.addWidget(self.lbl_status)
        
        self.setLayout(layout)
        self.resize(200, 120)
        
        # Position top right
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, 20)
        
    def update_info(self, fps: float, gesture_name: str, is_paused: bool):
        self.lbl_fps.setText(f"FPS: {fps:.1f}")
        self.lbl_gesture.setText(f"Gesture: {gesture_name}")
        self.lbl_status.setText(f"Status: {'Paused' if is_paused else 'Active'}")
        
        if is_paused:
            self.lbl_status.setStyleSheet("color: #FF5555;")
        else:
            self.lbl_status.setStyleSheet("color: #55FF55;")

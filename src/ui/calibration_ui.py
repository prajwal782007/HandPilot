from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class CalibrationUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180); color: white;")
        
        # Make it full screen
        self.showFullScreen()
        
        layout = QVBoxLayout()
        self.label = QLabel("Calibration Mode")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial", 24, QFont.Weight.Bold)
        self.label.setFont(font)
        
        self.instruction = QLabel("Move your hand to the TOP LEFT corner and pinch.")
        self.instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_inst = QFont("Arial", 16)
        self.instruction.setFont(font_inst)
        
        layout.addWidget(self.label)
        layout.addWidget(self.instruction)
        
        self.setLayout(layout)
        
    def update_step(self, points_collected: int):
        instructions = [
            "Move your hand to the TOP LEFT corner and pinch.",
            "Move your hand to the TOP RIGHT corner and pinch.",
            "Move your hand to the BOTTOM LEFT corner and pinch.",
            "Move your hand to the BOTTOM RIGHT corner and pinch.",
            "Calibration Complete!"
        ]
        
        if points_collected < len(instructions):
            self.instruction.setText(instructions[points_collected])
            
        if points_collected == 4:
            # Auto-close after a short delay
            # In a real app we'd use QTimer, this is a simplified version
            pass

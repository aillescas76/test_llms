from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt

class InputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Select a model first...")
        
        self.setStyleSheet("""
            QTextEdit {
                background: #3E3E3E;
                color: #DEDEDE;
                border-radius: 8px;
                border: 1px solid #4A4A4A;
                padding: 12px;
                min-height: 200px;
            }
        """)
        
        self.layout.addWidget(QLabel("Input Text:"))
        self.layout.addWidget(self.input_text)
        self.setLayout(self.layout)

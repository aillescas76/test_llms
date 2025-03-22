from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser

class ResultWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.result_display = QTextBrowser()
        self.result_display.setStyleSheet("""
            QTextBrowser {
                background: #3E3E3E;
                color: #DEDEDE;
                border-radius: 8px;
                border: 1px solid #4A4A4A;
                padding: 12px;
            }
        """)
        
        self.layout.addWidget(QLabel("Response Output:"))
        self.layout.addWidget(self.result_display)
        self.setLayout(self.layout)

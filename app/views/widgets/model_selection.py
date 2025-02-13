from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel

class ModelSelectionWidget(QWidget):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.model_list = QListWidget()
        self.model_list.addItems([model['name'] for model in self.models])
        self.layout.addWidget(QLabel("Select LLM Model:"))
        self.layout.addWidget(self.model_list)
        self.setLayout(self.layout)
        self.setStyleSheet("""
            QListWidget {
                background: #3E3E3E;
                color: #DEDEDE;
                border-radius: 8px;
                border: 1px solid #4A4A4A;
                padding: 8px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background: #34495E;
            }
            QListWidget::item:selected {
                background: #1ABC9C;
                border: 1px solid #16A085;
            }
        """)

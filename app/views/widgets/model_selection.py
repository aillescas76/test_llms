from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QComboBox
from PyQt6.QtCore import Qt

class ModelSelectionWidget(QWidget):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        # Organize models by provider.
        self.models_by_provider = {}
        for model in self.models:
            provider = model.get("provider", "unknown")
            self.models_by_provider.setdefault(provider, []).append(model)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # Create a dropdown for provider selection.
        self.layout.addWidget(QLabel("Select Provider:"), alignment=Qt.AlignmentFlag.AlignLeft)
        self.provider_combo = QComboBox(self)
        self.provider_combo.addItems(sorted(self.models_by_provider.keys()))
        self.layout.addWidget(self.provider_combo)
        
        # Create a list widget to display models for the selected provider.
        self.layout.addWidget(QLabel("Select LLM Model:"), alignment=Qt.AlignmentFlag.AlignLeft)
        self.model_list = QListWidget(self)
        self.layout.addWidget(self.model_list)

        # Update the model list based on the selected provider.
        self.provider_combo.currentTextChanged.connect(self.update_model_list)
        self.update_model_list(self.provider_combo.currentText())

        self.setLayout(self.layout)
        self.setStyleSheet("""
            QComboBox, QListWidget {
                background: #3E3E3E;
                color: #DEDEDE;
                border-radius: 8px;
                padding: 8px;
            }
            QComboBox::drop-down {
                border: none;
            }
            /* Style the dropdown list for dark mode */
            QComboBox QAbstractItemView {
                background-color: #3E3E3E;
                border: 1px solid #3E3E3E;
                selection-background-color: #1ABC9C;
                selection-color: #DEDEDE;
                color: #DEDEDE;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background: #1ABC9C;
                border: 1px solid #16A085;
            }
            QListWidget::item:hover {
                background: #34495E;
            }
        """)

    def update_model_list(self, provider: str):
        """
        Update the model list to show only models from the selected provider.
        """
        self.model_list.clear()
        for model in self.models_by_provider.get(provider, []):
            self.model_list.addItem(model['name'])

    def selected_model(self) -> str:
        """
        Return the currently selected model name.
        """
        current_item = self.model_list.currentItem()
        return current_item.text() if current_item else ""

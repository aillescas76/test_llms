from PyQt6.QtWidgets import (QMainWindow, QHBoxLayout, QWidget, QSizePolicy, QPushButton, QMessageBox, QDialog, QVBoxLayout, QTextEdit)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
import logging
from datetime import datetime
from app.models.config import load_config
from app.services.provider_manager import ProviderManager
from app.views.widgets.model_selection import ModelSelectionWidget
from app.views.widgets.input_widget import InputWidget
from app.views.widgets.result_widget import ResultWidget

class Worker(QThread):
    finished = pyqtSignal(tuple)  # (response, reasoning)
    error = pyqtSignal(Exception)
    
    def __init__(self, provider_manager, model_name, prompt):
        super().__init__()
        self.provider_manager = provider_manager
        self.model_name = model_name
        self.prompt = prompt

    def run(self):
        try:
            logging.info(f"Starting LLM call to {self.model_name}")
            result = self.provider_manager.get_response(self.model_name, self.prompt)
            self.finished.emit(result)
            logging.info(f"Completed LLM call to {self.model_name}")
        except Exception as e:
            self.error.emit(e)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('MainWindow')
        self.config = load_config()
        self.provider_manager = ProviderManager(self.config)
        self.setWindowTitle("LLM Chat Interface")
        self.setMinimumSize(1280, 720)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Create panels with equal stretch
        self.model_panel = ModelSelectionWidget(self.config['models'])
        self.input_panel = InputWidget()
        self.output_panel = ResultWidget()
        
        # Set equal size policies
        for panel in [self.model_panel, self.input_panel, self.output_panel]:
            panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            panel.setMinimumWidth(300)
        
        # Create arrow button
        self.process_btn = QPushButton("→")
        self.process_btn.setFixedSize(40, 40)
        self.process_btn.setEnabled(False)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #1ABC9C;
                color: #ECF0F1;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
            QPushButton:disabled {
                background-color: #34495E;
                color: #7F8C8D;
            }
        """)
        
        # Add widgets to layout
        layout.addWidget(self.model_panel, stretch=1)
        layout.addWidget(self.input_panel, stretch=3)
        layout.addWidget(self.process_btn, stretch=0)
        layout.addWidget(self.output_panel, stretch=3)
        
        # Connect signals
        self.process_btn.clicked.connect(self.process_input)
        self.model_panel.model_list.itemClicked.connect(self.on_model_selected)
        
        # Visual styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2D2D2D;
            }
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #DEDEDE;
            }
        """)

    def on_model_selected(self, item):
        self.selected_model = item.text()
        self.input_panel.setEnabled(True)
        self.input_panel.input_text.setPlaceholderText(f"Enter text to process with {self.selected_model}...")
        self.process_btn.setEnabled(True)

    def show_reasoning_window(self, content):
        dialog = QDialog(self)
        dialog.setWindowTitle("Reasoning Details")
        dialog.setMinimumSize(600, 400)
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setPlainText(content)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("""
            QTextEdit {
                background: #3E3E3E;
                color: #DEDEDE;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        layout.addWidget(text_edit)
        dialog.setLayout(layout)
        dialog.exec()

    def _save_request(self, prompt):
        """Save user request to file with timestamp"""
        try:
            with open('.requests.txt', 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().isoformat()}] {self.selected_model} Request:\n{prompt}\n\n")
        except Exception as e:
            self.logger.error(f"Error saving request: {str(e)}")

    def _save_response(self, prompt, response):
        """Save full interaction to response file"""
        try:
            with open('.response.txt', 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().isoformat()}] {self.selected_model} Interaction:\n")
                f.write(f"User: {prompt}\n")
                f.write(f"AI: {response}\n\n")
        except Exception as e:
            self.logger.error(f"Error saving response: {str(e)}")

    def process_input(self):
        self.process_btn.setEnabled(False)
        self.process_btn.setText("...")
        self.processing_id = f"[{datetime.now().strftime('%H:%M:%S')}] Processing..."
        self.output_panel.result_display.append(self.processing_id)
        
        text = self.input_panel.input_text.toPlainText().strip()
        if not text:
            self.show_error("Please enter some text")
            self.process_btn.setEnabled(True)
            self.process_btn.setText("→")
            return

        try:
            # Save request before starting thread
            self._save_request(text)
            self.logger.info(f"Starting request to {self.selected_model}")
            
            # Create worker thread
            self.worker = Worker(self.provider_manager, self.selected_model, text)
            self.worker.finished.connect(self.handle_response)
            self.worker.error.connect(self.handle_error)
            self.worker.start()
            
        except Exception as e:
            self.logger.error(f"Error starting thread: {str(e)}")
            self.show_error(str(e))
            self.reset_ui_state()

    def handle_response(self, result):
        """Handle successful response from worker thread"""
        try:
            response, reasoning = result
            self.output_panel.result_display.append(
                f"[{datetime.now().strftime('%H:%M')}] {self.selected_model} Response:\n{response}\n"
            )
            user_input = self.input_panel.input_text.toPlainText().strip()
            if reasoning:
                self.show_reasoning_window(reasoning)
                self._save_response(f"<Deepseek reasoning>{user_input}", response)
            
            # Save the full interaction
            self._save_response(user_input, response)
            
        except Exception as e:
            self.logger.error(f"Error handling response: {str(e)}")
        finally:
            self.reset_ui_state()

    def handle_error(self, error):
        """Handle errors from worker thread"""
        self.logger.error(f"Error in {self.selected_model} request: {str(error)}")
        self.show_error(f"API Error: {str(error)}")
        self.reset_ui_state()

    def reset_ui_state(self):
        """Reset UI elements after processing"""
        self.process_btn.setEnabled(True)
        self.process_btn.setText("→")
        self.input_panel.input_text.clear()
        # Remove processing message
        current_text = self.output_panel.result_display.toPlainText()
        self.output_panel.result_display.setPlainText(
            current_text.replace(self.processing_id, "")
        )

    def show_error(self, message):
        QMessageBox.critical(
            self,
            "Error",
            message,
            QMessageBox.StandardButton.Ok
        )

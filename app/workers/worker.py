from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot
import logging
from dataclasses import dataclass

@dataclass
class WorkerResult:
    response: str
    reasoning: str

class WorkerSignals(QObject):
    finished = pyqtSignal(object)  # will emit a WorkerResult instance
    error = pyqtSignal(Exception)

class Worker(QRunnable):
    """
    Worker thread for processing LLM requests.
    """
    def __init__(self, provider_manager, model_name: str, prompt: str) -> None:
        super().__init__()
        self.provider_manager = provider_manager
        self.model_name = model_name
        self.prompt = prompt
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self) -> None:
        """
        Execute the background task.
        """
        try:
            logging.info(f"Starting LLM call to {self.model_name}")
            # Get the response as a tuple and convert to a WorkerResult.
            response, reasoning = self.provider_manager.get_response(self.model_name, self.prompt)
            result = WorkerResult(response=response, reasoning=reasoning)
            self.signals.finished.emit(result)
            logging.info(f"Completed LLM call to {self.model_name}")
        except Exception as e:
            self.signals.error.emit(e)

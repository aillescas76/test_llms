import sys
import logging
from multiprocessing import Process
from PyQt6.QtWidgets import QApplication
from app.views.main_window import MainWindow
from app.services.communications import CommunicationManager
from app.services.voice_feedback import run_voice_feedback

# Add logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)

def main():
    app = QApplication(sys.argv)
    comm_manager = CommunicationManager()
    feedback_process = Process(target=run_voice_feedback, args=(comm_manager,), daemon=True)
    feedback_process.start()
    window = MainWindow(comm_manager)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

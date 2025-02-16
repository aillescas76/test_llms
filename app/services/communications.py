import enum
from multiprocessing import Queue
from typing import Any, Dict, Optional, Union
import multiprocessing

class MessageType(enum.Enum):
    INPUT = "input"
    OUTPUT = "output"
    LOG = "log"
    ERROR = "error"

class CommunicationManager:
    def __init__(self):
        # Create dedicated queues for each message type.
        self.queues: Dict[str, Queue] = {
            MessageType.INPUT.value: multiprocessing.Queue(),
            MessageType.OUTPUT.value: multiprocessing.Queue(),
            MessageType.LOG.value: multiprocessing.Queue(),
            MessageType.ERROR.value: multiprocessing.Queue()
        }

    def send_message(self, msg_type: Union[MessageType, str], payload: Any) -> None:
        # Convert enum to string if needed.
        if isinstance(msg_type, MessageType):
            msg_type = msg_type.value

        # Optionally, you can check if msg_type is known; here we create one if necessary.
        if msg_type not in self.queues:
            self.queues[msg_type] = multiprocessing.Queue()

        message = {
            "type": msg_type,
            "payload": payload
        }
        self.queues[msg_type].put(message)

    def get_message(self, msg_type: Union[MessageType, str], timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        if isinstance(msg_type, MessageType):
            msg_type = msg_type.value

        if msg_type not in self.queues:
            return None

        try:
            message = self.queues[msg_type].get(timeout=timeout)
            return message
        except Exception:
            return None

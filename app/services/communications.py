import enum
import time
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
            
    def get_message_from_types(self, msg_types: list, timeout: Optional[float] = None) -> Optional[tuple]:
        """
        Polls the queues corresponding to a list of MessageType (or string) values and returns
        the first message that appears as a tuple: (message, message_type).
        Returns None if no message is received within the specified timeout.
        """
        # Convert any MessageType to its string value.
        msg_types = [mt.value if hasattr(mt, "value") else mt for mt in msg_types]
        start_time = time.perf_counter()
        while True:
            for msg_type in msg_types:
                if msg_type not in self.queues:
                    continue
                try:
                    # Try retrieving the message non-blocking.
                    message = self.queues[msg_type].get_nowait()
                    return message, msg_type
                except Exception:
                    continue
            if timeout is not None and (time.perf_counter() - start_time) >= timeout:
                return None
            time.sleep(0.05)  # Short sleep to avoid busy polling.

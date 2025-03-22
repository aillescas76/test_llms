from random import choice
import multiprocessing

from elevenlabs import ElevenLabs, stream

from app.services.provider_manager import ProviderManager
from app.services.communications import CommunicationManager, MessageType

MARIA = "frWnbHZZPAIOUOfRlRLx"
HECTOR = "QRCFBz1ziQa0tsr2mnML"
def generate_summary_input(text: str) -> str:
    """
    Uses a summary model (the first with summary=True in its config) to generate a friendly summary of the provided text.
    """
    summary_pm = ProviderManager.get_summary_provider_manager()
    # Assuming the summary provider manager contains only one model.
    model_name = next(iter(summary_pm.providers))
    prompt = (
        f"Act as a friend that get the following request:\n '''{text}'''\n"
        "Respond in a casual way, keeping the language of the text, but do not provide"
        " a full response, just act as you want to get some time to think in the response,"
        " BE BRIEF and do not give any concrete timeline,"
        " we do not want to keep talking when the analysis is already done :-)"
    )
    response, _ = summary_pm.get_response(model_name, prompt)
    return response

def generate_summary_output(text: str) -> str:
    """
    Uses a summary model to generate a precise summary of the provided text.
    """
    summary_pm = ProviderManager.get_summary_provider_manager()
    # Assuming the summary provider manager contains only one model.
    model_name = next(iter(summary_pm.providers))
    prompt = (
        "You have been given a response to an user question. "
        "Provide a concise and precise summary that highlights the key points."
        "Keep the same language as the text."
        f"Act as an expert summarizer with precision for the following text:\n '''{text}'''\n"
    )
    response, _ = summary_pm.get_response(model_name, prompt)
    return response

def run_voice_feedback(comm_manager):
    """
    Process that handles voice feedback by monitoring the output queue
    and converting messages to speech.
    
    Args:
        comm_manager: Instance of CommunicationManager to handle message queues
    """
    # Initialize the ElevenLabs client with your API key
    eleven_client = ElevenLabs()
    # Map message type strings to their corresponding summary functions.
    summary_funcs = {
        MessageType.INPUT.value: generate_summary_input,
        MessageType.OUTPUT.value: generate_summary_output,
    }
    while True:
        try:
            # Poll for a message from either INPUT or OUTPUT queues.
            result = comm_manager.get_message_from_types([MessageType.INPUT, MessageType.OUTPUT], timeout=1)
            if result:
                message, msg_type = result  # msg_type will be a string, e.g., "input" or "output"
                if message and "payload" in message:
                    print(f"Summarizing {msg_type} message\n")
                    summary = summary_funcs[msg_type](message['payload'])
                    audio_stream = eleven_client.generate(
                        text=summary,
                        voice=choice((MARIA, HECTOR)),
                        model="eleven_flash_v2_5"
                    )
                    stream(audio_stream)
        except Exception as e:
            print(f"Error in voice feedback: {str(e)}")

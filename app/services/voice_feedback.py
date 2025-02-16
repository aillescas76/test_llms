from app.services.communications import CommunicationManager, MessageType
import multiprocessing
from elevenlabs import ElevenLabs, play
import openai

def generate_summary(text: str) -> str:
    """
    Uses the OpenAI API to generate a concise summary of the provided text.
    """
    prompt = f"Please provide a concise summary of the following text:\n\n{text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def run_voice_feedback(comm_manager):
    """
    Process that handles voice feedback by monitoring the output queue
    and converting messages to speech.
    
    Args:
        comm_manager: Instance of CommunicationManager to handle message queues
    """
    # Initialize the ElevenLabs client with your API key
    eleven_client = ElevenLabs(api_key="YOUR_API_KEY")
    while True:
        try:
            message = comm_manager.get_message(MessageType.OUTPUT.value, timeout=5)
            if message and "payload" in message:
                # Generate summary using the OpenAI API
                summary = generate_summary(message['payload'])
                # Use ElevenLabs to convert the summary text to speech.
                audio = eleven_client.text_to_speech.convert(
                    voice_id="JBFqnCBsd6RMkjVDRZzb",
                    output_format="mp3_44100_128",
                    text=summary,
                    model_id="eleven_multilingual_v2",
                )
                play(audio)
        except Exception as e:
            print(f"Error in voice feedback: {str(e)}")

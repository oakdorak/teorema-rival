
from gradio_client import Client

try:
    client = Client("Qwen/Qwen3-TTS")
    print("Available functions:")
    client.view_api()
except Exception as e:
    print(f"Error: {e}")

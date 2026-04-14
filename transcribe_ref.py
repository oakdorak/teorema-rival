
import os
import requests
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
WHISPER_API_URL = "https://api.openai.com/v1/audio/transcriptions"
FILE_PATH = "/Users/robbit/Downloads/ssstik.io__subtitulosfreestyle_1776148728890.mp3"

try:
    with open(FILE_PATH, "rb") as audio_file:
        files = {
            "file": ("audio.mp3", audio_file, "audio/mpeg"),
            "model": (None, "whisper-1")
        }
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        response = requests.post(WHISPER_API_URL, files=files, headers=headers)
        if response.status_code == 200:
            print(response.json().get("text", ""))
        else:
            print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Exception: {e}")

import os
import time
import requests
import json
import base64
from datetime import datetime
from gradio_client import Client

OUTPUT_DIR = os.getenv("AUDIO_OUTPUT_DIR", "/tmp/audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class IntegradorAudio:
    def __init__(self):
        self.qwen_client = Client("Qwen/Qwen3-TTS")
        self.base_path = os.path.dirname(__file__)
        self.path_t = os.path.join(self.base_path, "assets/refs/teorema.mp3")
        self.path_g = os.path.join(self.base_path, "assets/refs/goku.mp3")
        self.txt_t = os.getenv("REF_TEXT_TEOREMA", "Siento que mi flow es la ley en la pista, nadie puede contra mi metrica.")
        self.txt_g = os.getenv("REF_TEXT_GOKU", "¡Hola, soy Goku! ¡Siento un ki impresionante en este lugar!")

    def generar_audio(self, texto, voice="alloy", filename_prefix="batalla"):
        if voice == "alloy":
            p, t, n = self.path_t, self.txt_t, "teorema"
        else:
            p, t, n = self.path_g, self.txt_g, "goku"
        
        if not os.path.exists(p):
            return {"error": f"No {n} in {p}"}

        try:
            res = self.qwen_client.predict(
                ref_audio=p,
                ref_text=t,
                target_text=texto,
                language="Auto",
                use_xvector_only=False,
                model_size="0.6B",
                api_name="/generate_voice_clone"
            )
            url = res[0]
            r = requests.get(url)
            if r.status_code == 200:
                return base64.b64encode(r.content).decode('utf-8')
            return {"error": "Down fail"}
        except Exception as e:
            return {"error": str(e)}

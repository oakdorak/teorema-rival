import os
import time
import requests
import json
import base64
from datetime import datetime

# Configuración
OUTPUT_DIR = os.getenv("AUDIO_OUTPUT_DIR", "/tmp/audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class IntegradorAudio:
    def __init__(self, tts_api_url=None):
        self.tts_api_url = tts_api_url or os.getenv("TTS_API_URL", "https://api.openai.com/v1/audio/speech")
        self.api_key = os.getenv("OPENAI_API_KEY", "")

    def generar_audio(self, texto, filename_prefix="batalla"):
        """
        Envía texto a la API de OpenAI TTS y devuelve el audio en formato Base64 o un mensaje de error.
        """
        if not self.api_key:
            return {"error": "Falta la OPENAI_API_KEY en las variables de entorno."}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}_{timestamp}.mp3")
        
        start_time = time.time()
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "tts-1",
                "input": texto,
                "voice": "alloy"
            }
            
            response = requests.post(
                self.tts_api_url,
                headers=headers,
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                latencia = time.time() - start_time
                self._log_interaccion(texto, output_path, latencia)
                return {"data": audio_base64}
            else:
                # Extraemos el mensaje de error detallado de OpenAI
                try:
                    err_msg = response.json().get("error", {}).get("message", response.text)
                except:
                    err_msg = response.text
                print(f"Error en API OpenAI TTS: {response.status_code} - {err_msg}")
                return {"error": f"OpenAI TTS ({response.status_code}): {err_msg}"}
                
        except Exception as e:
            print(f"Error en comunicación con OpenAI TTS: {e}")
            return {"error": f"Error de conexión TTS: {str(e)}"}

    def _log_interaccion(self, texto, path, latencia):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "texto": texto,
            "archivo_audio": path,
            "latencia_segundos": round(latencia, 3)
        }
        try:
            log_file = os.path.join(OUTPUT_DIR, "interacciones.jsonl")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass

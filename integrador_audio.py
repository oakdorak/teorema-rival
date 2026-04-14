import os
import time
import requests
import json
from datetime import datetime

# Configuración: Usamos /tmp para compatibilidad con Vercel
OUTPUT_DIR = os.getenv("AUDIO_OUTPUT_DIR", "/tmp/audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class IntegradorAudio:
    def __init__(self, tts_api_url=None):
        # Prioridad: Argumento > Variable de Entorno > Default OpenAI
        self.tts_api_url = tts_api_url or os.getenv("TTS_API_URL", "https://api.openai.com/v1/audio/speech")
        self.api_key = os.getenv("OPENAI_API_KEY", "")

    def generar_audio(self, texto, filename_prefix="batalla"):
        """
        Envía texto a la API de OpenAI TTS y guarda el archivo .mp3 resultante.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # OpenAI devuelve mp3 por defecto
        output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}_{timestamp}.mp3")
        
        start_time = time.time()
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Payload específico para OpenAI TTS
            payload = {
                "model": "tts-1",
                "input": texto,
                "voice": "alloy" # Puedes cambiar la voz: alloy, echo, fable, onyx, nova, shimmer
            }
            
            response = requests.post(
                self.tts_api_url,
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                
                latencia = time.time() - start_time
                self._log_interaccion(texto, output_path, latencia)
                return output_path
            else:
                print(f"Error en API OpenAI TTS: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error en comunicación con OpenAI TTS: {e}")
            return None

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

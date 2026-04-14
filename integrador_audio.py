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
        # Prioridad: Argumento > Variable de Entorno > Default localhost
        self.tts_api_url = tts_api_url or os.getenv("TTS_API_URL", "http://localhost:8000")

    def generar_audio(self, texto, filename_prefix="batalla"):
        """
        Envía texto a la API de RVC/TTS y guarda el archivo .wav resultante.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}_{timestamp}.wav")
        
        start_time = time.time()
        
        try:
            # Enviar solicitud a la API de TTS
            response = requests.post(
                f"{self.tts_api_url}/generate",
                json={"text": texto, "speaker": "teorema"},
                timeout=10
            )
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                
                latencia = time.time() - start_time
                self._log_interaccion(texto, output_path, latencia)
                return output_path
            else:
                print(f"Error en API TTS: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error en comunicación con TTS: {e}")
            return None

    def _log_interaccion(self, texto, path, latencia):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "texto": texto,
            "archivo_audio": path,
            "latencia_segundos": round(latencia, 3)
        }
        
        # En Vercel, los logs en archivo no persisten, pero los mantenemos para local
        try:
            log_file = os.path.join(OUTPUT_DIR, "interacciones.jsonl")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass

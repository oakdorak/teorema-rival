import os
import time
import requests
import json
import subprocess
from datetime import datetime

# Configuración
OUTPUT_DIR = "outputs/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class IntegradorAudio:
    def __init__(self, tts_api_url="http://localhost:8000"):
        self.tts_api_url = tts_api_url

    def generar_audio(self, texto, filename_prefix="batalla"):
        """
        Envía texto a la API de RVC/TTS y guarda el archivo .wav resultante.
        Maneja latencia mediante solicitud asíncrona (simulada) y logs.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}_{timestamp}.wav")
        
        start_time = time.time()
        
        try:
            # Enviar solicitud a la API local (RVC/TTS)
            # Adaptar según el endpoint real de tu servidor RVC
            response = requests.post(
                f"{self.tts_api_url}/generate",
                json={"text": texto, "speaker": "teorema"},
                timeout=5
            )
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                
                latencia = time.time() - start_time
                self._log_interaccion(texto, output_path, latencia)
                return output_path
            else:
                print(f"Error en API: {response.status_code}")
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
        
        log_file = os.path.join(OUTPUT_DIR, "interacciones.jsonl")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

# Ejemplo de uso:
# audio_gen = IntegradorAudio()
# ruta = audio_gen.generar_audio("Yo soy el teorema, rima suprema")

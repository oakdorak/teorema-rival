import os
import time
import requests
import json
import base64
from datetime import datetime
from gradio_client import Client

# Configuración
OUTPUT_DIR = os.getenv("AUDIO_OUTPUT_DIR", "/tmp/audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class IntegradorAudio:
    def __init__(self):
        # Usamos el Space de Qwen3-TTS para clonación Zero-Shot
        self.qwen_client = Client("Qwen/Qwen3-TTS")
        
        # URLs de los audios de referencia (Debe configurarlas el usuario en Vercel)
        self.ref_teorema = os.getenv("REF_AUDIO_TEOREMA", "")
        self.ref_goku = os.getenv("REF_AUDIO_GOKU", "")

    def generar_audio(self, texto, voice="alloy", filename_prefix="batalla"):
        """
        Utiliza Qwen3-TTS para clonar la voz basándose en el audio de referencia.
        """
        ref_audio = self.ref_teorema if voice == "alloy" else self.ref_goku
        
        if not ref_audio:
            return {"error": f"Falta el audio de referencia para la voz {voice} (REF_AUDIO_...)"}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}_{timestamp}.mp3")
        
        start_time = time.time()
        
        try:
            # Llamada al Space de Qwen3-TTS
            # El API de Qwen3-TTS espera: texto, audio_referencia
            result = self.qwen_client.predict(
                text=texto,
                ref_audio=ref_audio,
                api_name="/predict"
            )
            
            # El resultado suele ser la ruta al archivo generado en el Space
            audio_url = result 
            
            # Descargamos el audio del Space para convertirlo a Base64
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(audio_response.content)
                
                audio_base64 = base64.b64encode(audio_response.content).decode('utf-8')
                latencia = time.time() - start_time
                self._log_interaccion(texto, output_path, latencia)
                return audio_base64
            else:
                return {"error": f"Error descargando audio de Qwen: {audio_response.status_code}"}
                
        except Exception as e:
            print(f"Error en Qwen3-TTS: {e}")
            return {"error": f"Error de clonación Qwen3: {str(e)}"}

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

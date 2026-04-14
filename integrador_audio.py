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
        
        # Obtenemos la URL base de la app
        self.base_url = os.getenv("VERCEL_URL", "localhost:8000")
        if not self.base_url.startswith("http"):
            self.base_url = f"https://{self.base_url}"

        # Rutas internas a los audios de referencia
        self.ref_teorema_url = f"{self.base_url}/refs/teorema.mp3"
        self.ref_goku_url = f"{self.base_url}/refs/goku.mp3"
        
        # Transcripciones de los audios de referencia
        self.text_teorema = os.getenv("REF_TEXT_TEOREMA", "Siento que mi flow es la ley en la pista, nadie puede contra mi metrica.")
        self.text_goku = os.getenv("REF_TEXT_GOKU", "¡Hola, soy Goku! ¡Siento un ki impresionante en este lugar!")

    def _download_ref_audio(self, url, name):
        """Descarga el audio de referencia a un archivo temporal."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                path = os.path.join(OUTPUT_DIR, f"ref_{name}.mp3")
                with open(path, "wb") as f:
                    f.write(response.content)
                return path
        except Exception as e:
            print(f"Error descargando audio de referencia {name}: {e}")
        return None

    def generar_audio(self, texto, voice="alloy", filename_prefix="batalla"):
        """
        Utiliza Qwen3-TTS para clonar la voz basándose en el audio de referencia.
        """
        if voice == "alloy":
            ref_url = self.ref_teorema_url
            ref_text = self.text_teorema
            name = "teorema"
        else:
            ref_url = self.ref_goku_url
            ref_text = self.text_goku
            name = "goku"
        
        local_ref_path = self._download_ref_audio(ref_url, name)
        if not local_ref_path:
            return {"error": f"No se pudo descargar la muestra de voz de {name} desde el servidor."}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}_{timestamp}.mp3")
        
        try:
            # Llamada optimizada al Space de Qwen3-TTS
            # Usamos model_size="0.6B" y language="Auto" para máxima estabilidad
            result = self.qwen_client.predict(
                ref_audio=local_ref_path,
                ref_text=ref_text,
                target_text=texto,
                language="Auto",
                use_xvector_only=False,
                model_size="0.6B",
                api_name="/generate_voice_clone"
            )
            
            audio_url = result[0]
            
            audio_res = requests.get(audio_url)
            if audio_res.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(audio_res.content)
                
                audio_b64 = base64.b64encode(audio_res.content).decode('utf-8')
                return audio_b64
            else:
                return {"error": f"Error descargando audio de Qwen: {audio_res.status_code}"}
                
        except Exception as e:
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

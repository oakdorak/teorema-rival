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
        
        # URLs de los audios de referencia (Configurar en Vercel)
        self.ref_teorema = os.getenv("REF_AUDIO_TEOREMA", "")
        self.ref_goku = os.getenv("REF_AUDIO_GOKU", "")
        
        # Transcripciones de los audios de referencia (Configurar en Vercel)
        # Qwen3-TTS requiere el texto exacto de lo que se dice en el audio de referencia
        self.text_teorema = os.getenv("REF_TEXT_TEOREMA", "Texto de referencia de Teorema")
        self.text_goku = os.getenv("REF_TEXT_GOKU", "Texto de referencia de Goku")

    def generar_audio(self, texto, voice="alloy", filename_prefix="batalla"):
        """
        Utiliza Qwen3-TTS para clonar la voz basándose en el audio de referencia.
        """
        # Seleccionamos la referencia según el modo
        if voice == "alloy": # Teorema
            ref_audio = self.ref_teorema
            ref_text = self.text_teorema
        else: # Goku
            ref_audio = self.ref_goku
            ref_text = self.text_goku
        
        if not ref_audio:
            return {"error": f"Falta el audio de referencia para la voz {voice} (REF_AUDIO_...)"}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}_{timestamp}.mp3")
        
        start_time = time.time()
        
        try:
            # Llamada al Space de Qwen3-TTS usando el API name correcto
            # Parámetros: ref_audio, ref_text, target_text, language, use_xvector_only, model_size
            result = self.qwen_client.predict(
                ref_audio=ref_audio,
                ref_text=ref_text,
                target_text=texto,
                language="Spanish",
                use_xvector_only=False,
                model_size="1.7B",
                api_name="/generate_voice_clone"
            )
            
            # El resultado es una tupla: (generated_audio_path, status)
            audio_url = result[0]
            
            # Descargamos el audio del Space para convertirlo a Base64
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(audio_response.content)
                
                audio_base64 = base64.b64encode(audio_//response.content).decode('utf-8')
                # Corrección de typo: audio_response.content
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

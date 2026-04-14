import os
import time
import requests
import json
import base64
from datetime import datetime
from gradio_client import Client

OUTPUT_DIR = os.getenv(\"AUDIO_OUTPUT_DIR\", \"/tmp/audio\")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class IntegradorAudio:
    def __init__(self):
        # Inicializamos el cliente con un timeout más largo si es posible
        self.qwen_client = Client(\"Qwen/Qwen3-TTS\")
        self.base_path = os.path.dirname(__file__)
        self.path_t = os.path.join(self.base_path, \"assets/refs/teorema.mp3\")
        self.path_g = os.path.join(self.base_path, \"assets/refs/goku.mp3\")
        
        # Textos de referencia EXACTOS para la clonación
        self.txt_t = os.getenv(\"REF_TEXT_TEOREMA\", \"Siento que mi flow es la ley en la pista, nadie puede contra mi metrica.\")
        self.txt_g = os.getenv(\"REF_TEXT_GOKU\", \"¡Hola, soy Goku! ¡Siento un ki impresionante en este lugar!\")

    def generar_audio(self, texto, voice=\"alloy\", filename_prefix=\"batalla\"):
        print(f\"[Audio] Generando voz para: {voice} | Texto: {texto[:30]}...\")
        
        if voice == \"alloy\":
            p, t, n = self.path_t, self.txt_t, \"teorema\"
        else:
            p, t, n = self.path_g, self.txt_g, \"goku\"
        
        if not os.path.exists(p):
            print(f\"[Audio Error] Archivo de referencia no encontrado: {p}\")
            return {\"error\": f\"No se encontró el archivo de referencia para {n} en {p}\"}

        try:
            # Llamada al modelo Qwen3-TTS
            print(f\"[Audio] Solicitando clonación a Qwen3 para {n}...\")
            res = self.qwen_client.predict(
                ref_audio=p,
                ref_text=t,
                target_text=texto,
                language=\"Auto\",
                use_xvector_only=False,
                model_size=\"0.6B\",
                api_name=\"/generate_voice_clone\"
            )
            
            if not res or not isinstance(res, (list, tuple)):
                print(f\"[Audio Error] Respuesta inesperada de Qwen3: {res}\")
                return {\"error\": \"Respuesta vacía o inválida del servidor de audio\"}
                
            url = res[0]
            print(f\"[Audio] URL de audio recibida: {url}\")
            
            # Descarga del archivo generado
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                print(f\"[Audio] Descarga exitosa. Tamaño: {len(r.content)} bytes\")
                return base64.b64encode(r.content).decode('utf-8')
            
            print(f\"[Audio Error] Fallo en descarga de URL. Status: {r.status_code}\")
            return {\"error\": f\"Fallo en la descarga del audio generado (HTTP {r.status_code})\"}
            
        except Exception as e:
            print(f\"[Audio Critical Error] {str(e)}\")
            return {\"error\": f\"Error crítico en IntegradorAudio: {str(e)}\"}

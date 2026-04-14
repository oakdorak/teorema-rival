import os
import json
import asyncio
import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional

# Importamos los motores
from generador_freestyle import GeneradorFreestyle
from integrador_audio import IntegradorAudio

app = FastAPI()

# Configuración de API Keys y Endpoints
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
WHISPER_API_URL = os.getenv("WHISPER_API_URL", "https://api.openai.com/v1/audio/transcriptions")

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

# Configuración de motores
motor_freestyle = GeneradorFreestyle(api_key=OPENAI_API_KEY)
audio_integrador = IntegradorAudio()

async def transcribe_audio(audio_bytes):
    """
    Envía los bytes de audio a la API de OpenAI Whisper y devuelve el texto.
    """
    try:
        files = {
            "file": ("audio.wav", audio_bytes, "audio/wav"),
            "model": (None, "whisper-1")
        }
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: requests.post(WHISPER_API_URL, files=files, headers=headers, timeout=15)
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "")
        else:
            print(f"Error en API OpenAI Whisper: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error en transcripción OpenAI Whisper: {e}")
        return None

@app.get("/")
async def get():
    try:
        with open(INDEX_PATH, "r") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<h1>index.html not found</h1>")

@app.post("/api/chat")
async def chat_endpoint(
    text: Optional[str] = Form(None), 
    file: Optional[UploadFile] = File(None),
    mode: Optional[str] = Form("teorema")
):
    """
    Endpoint HTTP que reemplaza el WebSocket para compatibilidad con Vercel.
    """
    try:
        input_text = ""
        
        # 1. Obtener el texto (ya sea por texto directo o por audio)
        if file:
            audio_bytes = await file.read()
            transcription = await transcribe_audio(audio_bytes)
            if transcription:
                input_text = transcription
            else:
                return JSONResponse(status_code=400, content={"error": "No se pudo transcribir el audio. Verifica tu API Key de OpenAI."})
        elif text:
            input_text = text
        else:
            return JSONResponse(status_code=400, content={"error": "Debes enviar texto o audio."})

        # 2. Generar respuesta freestyle según el modo (Ahora con LLM real)
        response_text = motor_freestyle.generar_cuarteta(input_text, mode=mode)
        
        # 3. Generar audio response (Cambiamos voz según modo)
        # Usamos voces de OpenAI como proxy hasta tener el RVC
        voice = "onyx" if mode == "goku" else "alloy"
        
        loop = asyncio.get_event_loop()
        audio_result = await loop.run_in_executor(
            None, 
            lambda: audio_integrador.generar_audio(response_text, voice=voice)
        )
        
        if isinstance(audio_result, dict) and "error" in audio_result:
            return JSONResponse(status_code=500, content={"error": audio_result["error"]})
        
        if not audio_result:
            return JSONResponse(status_code=500, content={"error": "Error desconocido generando audio TTS."})

        return {
            "text": response_text,
            "audio_base64": audio_result,
            "transcription": input_text if file else None
        }
        
    except Exception as e:
        print(f"Error en chat_endpoint: {e}")
        return JSONResponse(status_code=500, content={"error": f"Error interno: {str(e)}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

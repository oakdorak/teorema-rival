import os
import json
import asyncio
import requests
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Importamos los motores
from generador_freestyle import GeneradorFreestyle
from integrador_audio import IntegradorAudio

app = FastAPI()

# Configuración de motores
motor_freestyle = GeneradorFreestyle(agresividad=0.8)
audio_integrador = IntegradorAudio()

# Configuración de Whisper (Open Whisper)
WHISPER_API_URL = os.getenv("WHISPER_API_URL", "http://localhost:8001/transcribe")
WHISPER_API_KEY = os.getenv("WHISPER_API_KEY", "")

async def transcribe_audio(audio_bytes):
    """
    Envía los bytes de audio a la API de Open Whisper y devuelve el texto.
    """
    try:
        # Simulamos el envío de un archivo de audio mediante multipart/form-data
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        headers = {"Authorization": f"Bearer {WHISPER_API_KEY}"} if WHISPER_API_KEY else {}
        
        # Ejecutamos la petición en un hilo para no bloquear el loop de FastAPI
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: requests.post(WHISPER_API_URL, files=files, headers=headers, timeout=15)
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "")
        else:
            print(f"Error en API Whisper: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error en transcripción Whisper: {e}")
        return None

@app.get("/")
async def get():
    with open("index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Recibimos datos (pueden ser texto o bytes)
            message = await websocket.receive()
            
            # 1. Obtener el texto de entrada
            input_text = ""
            if "text" in message:
                input_text = message["text"]
            elif "bytes" in message:
                # Es audio -> Transcribir con Open Whisper
                audio_bytes = message["bytes"]
                transcription = await transcribe_audio(audio_bytes)
                if transcription:
                    input_text = transcription
                else:
                    await websocket.send_json({"error": "No se pudo transcribir el audio"})
                    continue
            
            if not input_text:
                continue

            # 2. Generar Punchline (Motor Freestyle)
            response_text = motor_freestyle.generar_cuarteta(input_text)
            
            # 3. TTS Response (Generar Audio)
            # Ejecutamos en executor para no bloquear
            loop = asyncio.get_event_loop()
            audio_path = await loop.run_in_executor(
                None, 
                lambda: audio_integrador.generar_audio(response_text)
            )
            
            # Enviar respuesta
            await websocket.send_json({
                "text": response_text,
                "audio_path": audio_path,
                "transcription": input_text if "bytes" in message else None
            })
            
    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error en WebSocket: {e}")

# Para desarrollo local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

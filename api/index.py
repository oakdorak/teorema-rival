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

# Configuración de OpenAI Whisper
WHISPER_API_URL = os.getenv("WHISPER_API_URL", "https://api.openai.com/v1/audio/transcriptions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

async def transcribe_audio(audio_bytes):
    """
    Envía los bytes de audio a la API de OpenAI Whisper y devuelve el texto.
    """
    try:
        # OpenAI requiere el parámetro 'model' y el archivo en multipart/form-data
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
    with open("index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive()
            
            input_text = ""
            if "text" in message:
                input_text = message["text"]
            elif "bytes" in message:
                audio_bytes = message["bytes"]
                transcription = await transcribe_audio(audio_bytes)
                if transcription:
                    input_text = transcription
                else:
                    await websocket.send_json({"error": "No se pudo transcribir el audio con OpenAI"})
                    continue
            
            if not input_text:
                continue

            response_text = motor_freestyle.generar_cuarteta(input_text)
            
            loop = asyncio.get_event_loop()
            audio_path = await loop.run_in_executor(
                None, 
                lambda: audio_integrador.generar_audio(response_text)
            )
            
            await websocket.send_json({
                "text": response_text,
                "audio_path": audio_path,
                "transcription": input_text if "bytes" in message else None
            })
            
    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error en WebSocket: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Teorema-Rival Backend (Refactorizado con Motor Freestyle e Integración Audio)

import os
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
# Importamos nuestras nuevas clases
from generador_freestyle import GeneradorFreestyle
from integrador_audio import IntegradorAudio

app = FastAPI()

# Inicialización de motores
motor_freestyle = GeneradorFreestyle(agresividad=0.8)
audio_integrador = IntegradorAudio(tts_api_url="http://localhost:8000")

@app.get("/")
async def get():
    with open("index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        
        # 1. Analizar e identificar (Tribe V2 logic goes here)
        # 2. Generar Punchline (Motor Freestyle)
        response_text = motor_freestyle.generar_cuarteta(data)
        
        # 3. TTS Response (Generar Audio)
        audio_path = audio_integrador.generar_audio(response_text)
        
        # Enviar respuesta tanto de texto como ruta de archivo para el frontend
        await websocket.send_json({
            "text": response_text,
            "audio_path": audio_path
        })

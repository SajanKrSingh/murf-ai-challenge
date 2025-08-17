# main.py

from fastapi import FastAPI, Form, Request, UploadFile, File, Path, HTTPException, WebSocket, WebSocketDisconnect

from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import assemblyai as aai
import google.generativeai as genai
from typing import Dict, List, Any

# Load environment variables from .env for secure API keys
load_dotenv()

app = FastAPI()

# --- Configure static files and HTML templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Load API Keys from environment variables
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Configure third-party APIs
if ASSEMBLYAI_API_KEY:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
else:
    print("Warning: ASSEMBLYAI_API_KEY not found in .env file.")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in .env file.")

# In-memory datastore for chat histories, keyed by session_id
chat_histories: Dict[str, List[Dict[str, Any]]] = {}


@app.get("/")
async def home(request: Request):
    """Serves the main HTML page for the application."""
    return templates.TemplateResponse("index.html", {"request": request})

# --- WebSocket Endpoint for real-time connections

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("New client connected.")
    
    audio_file_path = "recorded_audio.webm"
    
    try:
        with open(audio_file_path, "wb") as audio_file:
            while True:
                try:
                    message = await websocket.receive()
                except WebSocketDisconnect:
                    print("🔴 Client disconnected.")
                    break   # ✅ stop loop after disconnect

                # ✅ Handle both binary and text
                if "bytes" in message and message["bytes"] is not None:
                    audio_file.write(message["bytes"])
                elif "text" in message and message["text"] is not None:
                    print(f"📩 Text message from client: {message['text']}")

    except Exception as e:
        print(f"⚠ WebSocket error: {e}")
    finally:
        print(f"✅ Audio stream saved to {audio_file_path}")


@app.post("/agent/chat/{session_id}")
async def agent_chat(
    session_id: str = Path(..., description="The unique ID for the chat session."),
    audio_file: UploadFile = File(...)
):
    """
    Handles a full conversational turn for the agent.
    Process: STT -> LLM -> TTS, with chat history.
    """
    fallback_audio_path = "static/fallback.mp3"

    # Handle critical error: API keys are not configured
    if not (GEMINI_API_KEY and ASSEMBLYAI_API_KEY and MURF_API_KEY):
        return FileResponse(fallback_audio_path, media_type="audio/mpeg", headers={"X-Error": "true"})

    try:
        # Step 1: Transcribe audio to text using AssemblyAI SDK
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file.file)

        if transcript.status == aai.TranscriptStatus.error or not transcript.text:
            raise Exception(f"Transcription failed: {transcript.error or 'No speech detected'}")

        user_query_text = transcript.text
      
        # Step 2: Retrieve chat history and get a response from the Gemini LLM
        session_history = chat_histories.get(session_id, [])
        model = genai.GenerativeModel('gemini-1.5-flash')
      
        chat = model.start_chat(history=session_history)
        response = chat.send_message(user_query_text)
        llm_response_text = response.text

        # Step 3: Update chat history with the new turn
        chat_histories[session_id] = chat.history

        # Step 4: Convert LLM text response to speech with Murf AI
        murf_voice_id = "en-IN-priya"
        url = "https://api.murf.ai/v1/speech/generate"
        headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        payload = {
            "text": llm_response_text,
            "voiceId": murf_voice_id,
            "format": "MP3",
            "volume": "100%"
        }

        murf_response = requests.post(url, json=payload, headers=headers)
        murf_response.raise_for_status()
        response_data = murf_response.json()
        audio_url = response_data.get("audioFile")

        if audio_url:
            return JSONResponse(content={
                "audio_url": audio_url,
                "user_query_text": user_query_text,
                "llm_response_text": llm_response_text
            })
        else:
            raise Exception("Murf API did not return an audio file.")

    except Exception as e:
        # Handle all exceptions gracefully and return fallback audio
        print(f"An error occurred: {e}")
        return FileResponse(fallback_audio_path, media_type="audio/mpeg", headers={"X-Error": "true"})
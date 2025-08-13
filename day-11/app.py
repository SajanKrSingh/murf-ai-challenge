# main.py
from fastapi import FastAPI, Request, UploadFile, File, Path
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import assemblyai as aai
import google.generativeai as genai
from typing import Dict, List, Any

load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if ASSEMBLYAI_API_KEY:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

chat_histories: Dict[str, List[Dict[str, Any]]] = {}

# DAY 11: Naya function jo fallback audio generate karega
def generate_fallback_audio(error_message: str):
    try:
        fallback_text = "I'm having trouble connecting right now. Please try again."
        url = "https://api.murf.ai/v1/speech/generate"
        headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        payload = {"text": fallback_text, "voiceId": "en-US-natalie", "format": "MP3"}
        
        murf_response = requests.post(url, json=payload, headers=headers)
        murf_response.raise_for_status()
        
        audio_url = murf_response.json().get("audioFile")
        return JSONResponse(status_code=500, content={"error": error_message, "audio_url": audio_url})
    except Exception as e:
        print(f"Fallback audio generation bhi fail ho gaya: {e}")
        # Agar fallback audio bhi na ban paye, toh bina audio ke error bhejo
        return JSONResponse(status_code=500, content={"error": error_message, "audio_url": None})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/agent/chat/{session_id}")
async def agent_chat(
    session_id: str = Path(..., description="Chat session ka unique ID."),
    audio_file: UploadFile = File(...)
):
    if not (GEMINI_API_KEY and ASSEMBLYAI_API_KEY and MURF_API_KEY):
        return generate_fallback_audio("Server configuration error: API key missing.")

    try:
        # Step 1: Speech-to-Text
        try:
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(audio_file.file)
            if transcript.status == aai.TranscriptStatus.error:
                return generate_fallback_audio(f"Transcription failed: {transcript.error}")
            user_query_text = transcript.text
            if not user_query_text:
                return JSONResponse(status_code=400, content={"error": "I'm having trouble connecting right now."}) # Iska audio nahi banayenge
        except Exception as e:
            return generate_fallback_audio("Failed to transcribe audio.")

        # Step 2: LLM Response
        try:
            session_history = chat_histories.get(session_id, [])
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=session_history)
            response = chat.send_message(user_query_text)
            llm_response_text = response.text
            chat_histories[session_id] = chat.history
        except Exception as e:
            return generate_fallback_audio("Failed to get response from LLM.")

        # Step 3: Text-to-Speech
        try:
            url = "https://api.murf.ai/v1/speech/generate"
            headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
            payload = {"text": llm_response_text, "voiceId": "en-IN-priya", "format": "MP3"}
            murf_response = requests.post(url, json=payload, headers=headers)
            murf_response.raise_for_status()
            audio_url = murf_response.json().get("audioFile")
            if not audio_url:
                return generate_fallback_audio("Murf API did not return an audio file.")
        except Exception as e:
            return generate_fallback_audio("Failed to generate speech.")

        # Success response
        return JSONResponse(content={
            "audio_url": audio_url,
            "user_query_text": user_query_text,
            "llm_response_text": llm_response_text
        })
    except Exception as e:
        return generate_fallback_audio("An unexpected server error occurred.")
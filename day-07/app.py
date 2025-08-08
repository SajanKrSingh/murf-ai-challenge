# app.py

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware # Import CORS Middleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import time
import tempfile

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# --- ADDED: CORS Middleware ---
# This allows the browser to make requests to the server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)


# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load API Keys
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- Day 7: New Echo Bot v2 Endpoint ---
# This is the new endpoint that combines transcription and TTS.
@app.post("/tts/echo")
async def tts_echo(audio_file: UploadFile = File(...)):
    """
    1. Transcribes the incoming audio file using AssemblyAI's multi-step process.
    2. Sends the transcribed text to Murf AI to generate a new voice.
    3. Returns the URL of the newly generated audio file.
    """
    if not ASSEMBLYAI_API_KEY or not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key(s) not configured."})

    try:
        # Step 1: Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await audio_file.read())
            tmp_path = tmp.name
        
        # Step 2: Upload the temporary file to AssemblyAI
        upload_endpoint = "https://api.assemblyai.com/v2/upload"
        headers_assembly = {"authorization": ASSEMBLYAI_API_KEY}
        with open(tmp_path, "rb") as f:
            upload_response = requests.post(upload_endpoint, headers=headers_assembly, data=f)
        
        os.remove(tmp_path) # Clean up the temporary file

        if upload_response.status_code != 200:
            return JSONResponse(content={"error": "AssemblyAI upload failed"}, status_code=upload_response.status_code)

        audio_url = upload_response.json().get("upload_url")
        if not audio_url:
            return JSONResponse(content={"error": "AssemblyAI upload URL missing"}, status_code=500)

        # Step 3: Request transcription from AssemblyAI
        transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
        json_data = {"audio_url": audio_url}
        headers_assembly['content-type'] = 'application/json'
        
        transcript_response = requests.post(transcript_endpoint, json=json_data, headers=headers_assembly)
        if transcript_response.status_code != 200:
            return JSONResponse(content={"error": "AssemblyAI transcription request failed"}, status_code=transcript_response.status_code)

        transcript_id = transcript_response.json()["id"]
        
        # Step 4: Poll for transcription completion
        polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        while True:
            polling_response = requests.get(polling_endpoint, headers=headers_assembly)
            status = polling_response.json().get("status")

            if status == "completed":
                transcribed_text = polling_response.json()["text"]
                break
            elif status == "error":
                return JSONResponse(content={"error": "AssemblyAI transcription failed"}, status_code=500)
            
            time.sleep(2) # Wait for 2 seconds before polling again

        if not transcribed_text or not transcribed_text.strip():
            return JSONResponse(status_code=400, content={"error": "No speech detected in audio."})

        # Step 5: Send transcribed text to Murf AI for TTS
        murf_url = "https://api.murf.ai/v1/speech/generate"
        headers_murf = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        
        payload = {
            "voiceId": "en-US-natalie",
            "text": transcribed_text
        }
        
        murf_response = requests.post(murf_url, json=payload, headers=headers_murf)
        murf_response.raise_for_status()
        
        murf_json = murf_response.json()
        murf_audio_url = murf_json.get("audioUrl") or murf_json.get("audioFile") or murf_json.get("url")

        # Step 6: Return the new audio URL from Murf
        return {"audio_url": murf_audio_url}

    except requests.exceptions.HTTPError as http_err:
        # Better error handling to return the exact message from the API
        return JSONResponse(status_code=http_err.response.status_code, content={"error": "An API call failed", "details": http_err.response.json()})
    except Exception as e:
        print(f"An error occurred in /tts/echo: {e}") 
        return JSONResponse(status_code=500, content={"error": "An internal server error occurred", "details": str(e)})

# app.py

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import time
import tempfile
import google.generativeai as genai # Import the Gemini library

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load API Keys
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Load the new Gemini API Key

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-latest')


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- Day 7: Echo Bot v2 Endpoint ---
@app.post("/tts/echo")
async def tts_echo(audio_file: UploadFile = File(...)):
    # This function remains the same as Day 7
    if not ASSEMBLYAI_API_KEY or not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key(s) not configured."})
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await audio_file.read())
            tmp_path = tmp.name
        
        upload_endpoint = "https://api.assemblyai.com/v2/upload"
        headers_assembly = {"authorization": ASSEMBLYAI_API_KEY}
        with open(tmp_path, "rb") as f:
            upload_response = requests.post(upload_endpoint, headers=headers_assembly, data=f)
        os.remove(tmp_path)

        audio_url = upload_response.json().get("upload_url")
        transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
        json_data = {"audio_url": audio_url}
        headers_assembly['content-type'] = 'application/json'
        transcript_response = requests.post(transcript_endpoint, json=json_data, headers=headers_assembly)
        transcript_id = transcript_response.json()["id"]
        
        polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        while True:
            polling_response = requests.get(polling_endpoint, headers=headers_assembly)
            status = polling_response.json().get("status")
            if status == "completed":
                transcribed_text = polling_response.json()["text"]
                break
            elif status == "error":
                return JSONResponse(content={"error": "AssemblyAI transcription failed"}, status_code=500)
            time.sleep(2)

        if not transcribed_text or not transcribed_text.strip():
            return JSONResponse(status_code=400, content={"error": "No speech detected in audio."})

        murf_url = "https://api.murf.ai/v1/speech/generate"
        headers_murf = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        payload = {"voiceId": "en-US-natalie", "text": transcribed_text}
        murf_response = requests.post(murf_url, json=payload, headers=headers_murf)
        murf_response.raise_for_status()
        murf_audio_url = murf_response.json().get("audioUrl")
        return {"audio_url": murf_audio_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "An internal server error occurred", "details": str(e)})


# --- Day 8: New LLM Query Endpoint ---
# This is the new endpoint for today's task.
@app.post("/llm/query")
async def llm_query(text: str = Form(...)):
    """
    Accepts text as input, sends it to the Gemini LLM,
    and returns the generated response.
    """
    if not GEMINI_API_KEY:
        return JSONResponse(status_code=500, content={"error": "Gemini API key not configured."})
    
    try:
        # Send the text to the Gemini model
        response = model.generate_content(text)
        
        # Return the model's response
        return JSONResponse(content={"response": response.text})
        
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to get response from LLM.", "details": str(e)})


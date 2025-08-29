# 🎤 AI Voice Agent – #30DaysOfVoiceAgents Challenge

An end-to-end, AI-powered conversational voice bot built with Python, FastAPI, and a powerful stack of AI services: **AssemblyAI**, **Murf AI**, and **Google Gemini**.

This project is the result of the #30DaysOfVoiceAgents challenge, showcasing a rapid development journey from a simple script to a full-featured conversational agent with memory and a unique personality.

---

### ✨ Key Features

- **🎙️ Real-time Voice Interaction:** Record your voice directly in the browser.
- **📝 Accurate Transcription:** High-accuracy speech-to-text powered by AssemblyAI.
- **🧠 Context-Aware Conversations:** Maintain a continuous conversation with session-based memory, powered by Google Gemini.
- **🎭 AI with a Persona:** The agent has a defined personality ("Bolt," a witty assistant) thanks to system prompting.
- **🔊 Natural-Sounding Speech:** Generate realistic and expressive voice responses using Murf AI.
- **🛡️ Robust Error Handling:** Built to handle API or client-side failures gracefully.
- **🎨 Modern UI:** A clean, single-button conversational interface with animations for a seamless user experience.
- **🌐 Web Search Integration:** Uses SerpAPI for real-time web search context.
- **📦 Docker Support:** Easily containerize and deploy with the included Dockerfile.
- **⛈️ Weather Info (Day 27):** Added weather information service for voice queries.

---

### 📅 Project Journey: Day 1 – Day 27

| Day  | Task                        | Key Outcome                                               |
| :--: | --------------------------- | --------------------------------------------------------- |
|  1️⃣  | Project Setup               | Basic FastAPI server with an HTML/JS frontend.            |
|  2️⃣  | REST TTS API                | Created a backend endpoint for Murf AI's TTS.             |
|  3️⃣  | Play TTS Audio              | Added a UI to play the generated speech.                  |
|  4️⃣  | Echo Bot v1                 | Recorded and replayed the user's voice.                   |
|  5️⃣  | Send Audio to Server        | Uploaded and saved user recordings on the server.         |
|  6️⃣  | Server Transcription        | Integrated AssemblyAI for server-side transcription.      |
|  7️⃣  | Echo Bot v2                 | Used Murf AI's voice to echo back transcribed text.       |
|  8️⃣  | LLM Integration             | Added Google Gemini to generate text responses.           |
|  9️⃣  | Full Pipeline               | Connected the full Voice → LLM → Voice flow.              |
|  🔟  | Chat History                | Implemented session-based memory for context.             |
| 1️⃣1️⃣ | Error Handling              | Made the client and server resilient to failures.         |
| 1️⃣2️⃣ | UI Revamp                   | Designed a conversational UI with a dynamic button.       |
| 1️⃣3️⃣ | AI Persona & Docs           | Implemented System Prompting and created this README.     |
| 1️⃣4️⃣ | Streaming STT               | Added real-time streaming transcription.                  |
| 1️⃣5️⃣ | Improved Session Handling    | Enhanced user session and context management.             |
| 1️⃣6️⃣ | Voice Output Optimization    | Improved TTS playback and fallback handling.              |
| 1️⃣7️⃣ | WebSocket Integration        | Switched to WebSocket for low-latency voice streaming.    |
| 1️⃣8️⃣ | Frontend Polish             | Added animations and improved UX.                         |
| 1️⃣9️⃣ | API Rate Limiting           | Added basic rate limiting for API endpoints.              |
| 2️⃣0️⃣ | Modular Codebase            | Refactored into services for STT, TTS, LLM.               |
| 2️⃣1️⃣ | Persistent Uploads          | Improved audio file management and uploads.               |
| 2️⃣2️⃣ | WAV Output Support          | Added support for WAV output and playback.                |
| 2️⃣3️⃣ | Enhanced Error Logging      | Improved logging and error reporting.                     |
| 2️⃣4️⃣ | Environment Config          | Centralized config and environment variable management.   |
| 2️⃣5️⃣ | Web Search Integration      | Added SerpAPI for contextual web search answers.          |
| 2️⃣6️⃣ | Dockerization               | Added Dockerfile for easy deployment.                     |
| 2️⃣7️⃣ | Weather Info Service        | Added weather information service for voice queries.      |

---

### 🛠️ Tech Stack & Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript (MediaRecorder API)
- **STT (Speech-to-Text)**: [AssemblyAI](https://www.assemblyai.com/)
- **TTS (Text-to-Speech)**: [Murf AI](https://murf.ai/)
- **LLM (Large Language Model)**: [Google Gemini](https://ai.google.dev/)
- **Web Search**: [SerpAPI](https://serpapi.com/)
- **Weather Info**: OpenWeatherMap API (Day 27)
- **Containerization**: Docker

The application follows a simple voice-in, voice-out pipeline:

```plaintext
┌───────────────┐      ┌────────────────────┐      ┌────────────────────┐
│   User Voice  │  ───>│ STT (AssemblyAI)   │───> │ LLM (Google Gemini)│
└───────────────┘      └────────────────────┘      └─────────┬──────────┘
                                                             │
┌────────────────────┐      ┌────────────────────┐           │
│  Voice Response    │<───  │   TTS (Murf AI)    │<──────────┘
└────────────────────┘      └────────────────────┘
```

---

### 🚀 Local Setup and Installation

#### 1. File Structure

Ensure your project directory is organized as follows:

```
/project-folder/
├── app.py
├── .env
├── requirements.txt
├── Dockerfile
├── /static/
│   └── script.js
├── /templates/
│   └── index.html
├── /services/
│   ├── llm.py
│   ├── stt.py
│   ├── tts.py
│   └── weather.py
└── /uploads/
```

#### 2. Install Dependencies

Activate your Python virtual environment and install the required packages:

```bash
pip install -r requirements.txt
```

#### 3. Set Environment Variables

Create a `.env` file in the root of your project and add your API keys:

```
MURF_API_KEY="your_murf_api_key_here"
ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
GEMINI_API_KEY="your_gemini_api_key_here"
SERPAPI_API_KEY="your_serpapi_key_here"
OPENWEATHER_API_KEY="your_openweather_api_key_here"
```

#### 4. Start the Server

From the project root directory, run the following command:

```bash
uvicorn app:app --reload
```

The application will be accessible at **`http://127.0.0.1:8000`**.

#### 5. (Optional) Run with Docker

To build and run the containerized app:

```bash
docker build -t voice-agent .
docker run -p 8000:8000 --env-file .env voice
```

# 🎙️ Day 07: Echo Bot v2 - The Full Conversational Loop

Welcome to Day 7 of the **#30DaysOfVoiceAgents** challenge! This is a landmark day where we combine all the skills learned so far to create a true voice-in, voice-out experience.

The "Echo Bot v2" listens to what you say, understands it, and then repeats it back to you in a professional, AI-generated voice. This completes the fundamental loop of a conversational AI agent.



---

## ✨ Key Features

-   **End-to-End Voice Interaction:** The application now handles a full conversational turn: voice input is recorded, transcribed, used to generate a new voice, and then played back.
-   **Combined API Orchestration:** The backend seamlessly orchestrates calls between two powerful AI services:
    1.  **AssemblyAI** for accurate speech-to-text transcription.
    2.  **Murf AI** for high-quality, text-to-speech voice generation.
-   **New Backend Endpoint (`/tts/echo`):** A single, powerful FastAPI endpoint that manages the entire transcription and TTS process.
-   **Real-Time UI Feedback:** The user interface provides clear status updates throughout the process, from "Listening..." to "Thinking..." and finally "Here is my response!".
-   **Robust Transcription Logic:** Implements a reliable, multi-step process (upload, request, poll) to handle audio transcription with AssemblyAI.

---

## 🛠️ Tech Stack

-   **Backend:** Python, FastAPI, Uvicorn
-   **Transcription Service:** **AssemblyAI**
-   **Text-to-Speech Service:** **Murf AI**
-   **API Communication:** `requests`
-   **Environment Management:** `python-dotenv`
-   **Frontend:** HTML5, CSS3, JavaScript (`MediaRecorder` API)

---

## 🚀 Getting Started

Follow these steps to set up and run the Echo Bot v2 project.

### 1. Prerequisites

-   Python 3.8+ installed
-   A Murf AI account and API key
-   An AssemblyAI account and API key

### 2. Clone the Repository

```bash
git clone [https://github.com/SajanKrSingh/30-days-of-voice-agents.git](https://github.com/SajanKrSingh/30-days-of-voice-agents.git)
cd 30-days-of-voice-agents/day-07
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

Install all required Python libraries.

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the `day-07/` directory. This file must contain the API keys for both services.

```env
MURF_API_KEY="your_murf_ai_api_key_here"
ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
```

---

## ▶️ Run the Application

Start the FastAPI server using Uvicorn.

```bash
uvicorn app:app --reload
```

Open your web browser and navigate to:
`http://127.0.0.1:8000`

---

## 🧪 How to Use

1.  Click the **Start Recording** button (you may need to grant microphone permission).
2.  Speak a sentence clearly.
3.  Click the **Stop Recording** button.
4.  Wait a few moments while the status changes to "Thinking...".
5.  Listen as the Echo Bot repeats your sentence back to you in a new AI voice!

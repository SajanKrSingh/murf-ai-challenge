# 🎙️ Day 09: Full Conversational AI Pipeline

Welcome to Day 9 of the **#30DaysOfVoiceAgents** challenge! This project brings everything together into a complete, end-to-end conversational pipeline.

The application listens to a user's voice, transcribes the speech to text, sends that text to a Large Language Model (LLM) for an intelligent response, and finally converts the LLM's text response back into high-quality speech using a selected voice.

---

## ✨ Key Features

-   **End-to-End Voice Interaction:** A complete voice-in, voice-out loop. The agent can listen, think, and speak.
-   **Multi-API Orchestration:** The backend, powered by FastAPI, seamlessly manages requests between three different AI services:
    1.  **AssemblyAI** for speech-to-text transcription.
    2.  **Google Gemini** for generating intelligent responses.
    3.  **ElevenLabs** for high-quality text-to-speech synthesis.
-   **Dynamic Voice Selection:** The UI allows users to fetch and select from a list of available voices from the TTS provider.
-   **Contextual LLM Prompting:** The prompt sent to the Gemini LLM is structured to ensure the AI responds in the character of a helpful voice assistant.
-   **Separate TTS Functionality:** Includes a dedicated endpoint for direct text-to-speech generation.

---

## 🛠️ Tech Stack

-   **Backend:** Python, FastAPI, Uvicorn
-   **Transcription Service:** **AssemblyAI**
-   **LLM Service:** **Google Gemini**
-   **Text-to-Speech Service:** **ElevenLabs**
-   **API Communication:** `requests`
-   **Environment Management:** `python-dotenv`
-   **Frontend:** HTML, Tailwind CSS, JavaScript (`MediaRecorder` API)

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

-   Python 3.8+ installed
-   An AssemblyAI account and API key
-   A Google Gemini API key
-   An **ElevenLabs** account and API key

### 2. Clone the Repository

```bash
git clone [https://github.com/SajanKrSingh/30-days-of-voice-agents.git](https://github.com/SajanKrSingh/30-days-of-voice-agents.git)
cd 30-days-of-voice-agents/day-09
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

Install all required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the `day-09/` directory. This file must contain the API keys for all three services.

```env
ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
GEMINI_API_KEY="your_google_gemini_api_key_here"
ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"
```

---

## ▶️ Run the Application

Start the FastAPI server using Uvicorn.

```bash
uvicorn app:app --reload
```

Open your web browser and navigate to:
`http://12.0.0.1:8000`

---

## 🧪 How to Use

1.  The application will automatically load the available voices into the dropdown menus.
2.  In the **Voice Conversation** section, select a voice for the AI.
3.  Click the **Start Recording** button and speak your query.
4.  Click the **Stop Recording** button.
5.  The application will display your transcribed text and then play the AI's spoken response.

# 🎙️ Day 06: Implementing Speech-to-Text Transcription

Welcome to **Day 6** of the #30DaysOfVoiceAgents challenge! This is a pivotal day where our application learns to "listen." We've implemented server-side transcription, allowing the app to convert spoken audio into written text.

This update integrates **AssemblyAI**, a powerful third-party service, to perform accurate speech-to-text conversion. The recorded audio is now sent directly to the server, transcribed, and the resulting text is displayed back to the user in the UI.



## ✨ Key Features

* **Server-Side Transcription:** Audio recorded in the browser is sent to a new backend endpoint for transcription.

* **AssemblyAI Integration:** Leverages the AssemblyAI Python SDK to accurately convert speech to text.

* **New Backend Endpoint (`/transcribe/file`):** A dedicated FastAPI endpoint that accepts an audio file and returns the transcription text.

* **Direct Audio Processing:** The audio data is transcribed directly from the request stream, eliminating the need to save the file on the server first.

* **Real-Time UI Updates:** The interface now displays the transcribed text, providing a complete speech-to-text user experience.

* **Secure API Key Management:** Both Murf AI and AssemblyAI API keys are securely managed using a `.env` file.

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn

* **Transcription Service:** **AssemblyAI**

* **Text-to-Speech Service:** Murf AI

* **API Communication:** `requests`

* **Environment Management:** `python-dotenv`

* **Frontend:** HTML5, CSS3, JavaScript (`MediaRecorder` API)

## 🚀 Getting Started

Follow these steps to set up and run the project with its new transcription capabilities.

### 1. Prerequisites

* Python 3.8+ installed

* A Murf AI account and API key

* An **AssemblyAI** account and API key

### 2. Get Your AssemblyAI API Key

1. Sign up for a free account on the [AssemblyAI Dashboard](https://www.assemblyai.com/dashboard/signup).

2. Once logged in, you will find your API key on the main dashboard. Copy this key.

### 3. Clone the Repository

```
git clone [https://github.com/SajanKrSingh/30-days-of-voice-agents.git](https://github.com/SajanKrSingh/30-days-of-voice-agents.git)
cd 30-days-of-voice-agents/day-06

```

### 4. Create a Virtual Environment

```
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

```

### 5. Install Dependencies

Install all required libraries, including the new `assemblyai` package.

```
pip install -r requirements.txt

```

### 6. Set Up Environment Variables

Create or update the `.env` file in the `day-06/` directory. It should now contain keys for both Murf AI and AssemblyAI.

```
MURF_API_KEY="your_murf_ai_api_key_here"
ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"

```

## ▶️ Run the Application

Start the server using Uvicorn:

```
uvicorn main:app --reload

```

Open your browser and navigate to:
`http://127.0.0.1:8000`

## 🧪 How to Use

1. Navigate to the **"Speech to Text"** section on the page.

2. Click the **Start Recording** button (you may need to grant microphone permission).

3. Speak a clear message.

4. Click the **Stop Recording** button.

5. Watch as the status changes to "Transcribing..." and then see your spoken words appear in the text box below!

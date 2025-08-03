# 🎙️ Day 02: Professional Text-to-Speech Web App

Welcome to Day 2 of the **#30DaysOfVoiceAgents** challenge! Today, we've built a fully functional web application that converts user-provided text into high-quality, realistic speech using the Murf AI API.

This project not only fulfills the core task of creating a TTS endpoint but also wraps it in a polished, modern, and user-friendly interface for a complete user experience.

<!-- TODO: Add a screenshot of the new UI and replace this link -->

---

## ✨ Key Features

- **Backend API Endpoint:** Robust `/tts` endpoint built with FastAPI that accepts text input and processes it.
- **Murf AI Integration:** Secure communication with the Murf AI `/speech/generate` API to synthesize speech in real-time.
- **Dynamic Audio Playback:** The generated audio URL is sent back to the frontend and played directly in the browser for instant feedback.
- **Professional UI:** Sleek, modern user interface with enhanced styling and a focus on user experience.
- **Secure API Key Handling:** Utilizes a `.env` file to securely manage the Murf AI API key, keeping sensitive credentials out of the public source code.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **API Communication:** `requests`
- **Environment Management:** `python-dotenv`
- **Frontend:** HTML5, Advanced CSS3, JavaScript
- **Voice API:** Murf AI (Text-to-Speech)

---

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

- Python 3.8+ installed
- A Murf AI account and your personal API key

### 2. Clone the Repository

```bash
git clone https://github.com/SajanKrSingh/30-days-of-voice-agents.git
cd 30-days-of-voice-agents/day-02
```

### 3. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

Install all required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a file named `.env` in the `day-02/` directory. This file will store your secret API key.

Add your Murf API key to the `.env` file as follows:

```env
MURF_API_KEY="your_actual_murf_api_key_goes_here"
```

---

## ▶️ Run the Application

Once the setup is complete, start the web server using Uvicorn:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables hot-reloading, so the server will automatically restart whenever you make changes to the code.

Now, open your favorite web browser and navigate to:

```
http://127.0.0.1:8000
```

---

## 🧪 How to Use

1. You will be greeted with a clean, modern interface.
2. Type any message you want to convert to speech into the text input field.
3. Click the **Generate Voice** button.
4. After a brief moment, an audio player will appear with the generated speech. Press play to listen!

# 🎙️ Day 04: Advanced Voice Agent Features

Welcome to **Day 4** of the #30DaysOfVoiceAgents challenge! Today, we've enhanced our text-to-speech web app with advanced features, making your voice agent smarter and more interactive.

This update introduces new capabilities such as voice selection, adjustable speaking rate, and improved error handling, all seamlessly integrated into a refined user interface.



---

## ✨ Key Features

- **Voice Selection:** Choose from multiple professional voices provided by Murf AI for personalized speech output.
- **Adjustable Speaking Rate:** Easily control the speed of speech to suit your preferences.
- **Robust Error Handling:** Enhanced feedback for invalid input and API errors, ensuring a smooth user experience.
- **Backend API Enhancements:** FastAPI endpoint now supports voice and rate parameters for flexible TTS generation.
- **Secure API Key Management:** API keys remain protected using a `.env` file.
- **Modern UI Improvements:** Updated frontend with intuitive controls and responsive design.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **API Communication:** requests
- **Environment Management:** python-dotenv
- **Frontend:** HTML5, CSS3, JavaScript
- **Voice API:** Murf AI (Text-to-Speech)

---

## 🚀 Getting Started

Follow these steps to set up and run the enhanced project:

### 1. Prerequisites

- Python 3.8+ installed
- Murf AI account and API key

### 2. Clone the Repository

```bash
git clone https://github.com/SajanKrSingh/30-days-of-voice-agents.git
cd 30-days-of-voice-agents/day-04
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the `day-04/` directory and add your Murf API key:

```env
MURF_API_KEY="your_actual_murf_api_key_goes_here"
```

---

### ▶️ Run the Application

Start the server:

```bash
uvicorn main:app --reload
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 How to Use

1. Enter your text in the input field.
2. Select your preferred voice and adjust the speaking rate.
3. Click **Generate Voice**.
4. Listen to the generated speech using the audio player.

document.addEventListener("DOMContentLoaded", () => {
  // --- UI Elements ---
  const recordBtn = document.getElementById("recordBtn");
  const audioPlayer = document.getElementById("audioPlayer");
  const statusDisplay = document.getElementById("statusDisplay");
  const sessionIdSpan = document.getElementById("sessionId");
  const chatHistoryDiv = document.getElementById("chatHistory");
  const micIcon = recordBtn.querySelector(".mic-icon");
  const stopIcon = recordBtn.querySelector(".stop-icon");

  // --- State Variables ---
  let mediaRecorder;
  let recordedChunks = [];
  let sessionId;
  let currentState = "idle"; // Possible states: 'idle', 'recording', 'processing'

  // --- Session Management ---
  const urlParams = new URLSearchParams(window.location.search);
  sessionId = urlParams.get("session_id");
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    window.history.replaceState({}, "", `?session_id=${sessionId}`);
  }
  sessionIdSpan.textContent = `${sessionId.substring(0, 4)}...${sessionId.slice(
    -4
  )}`;

  // --- Event Listeners ---
  // When audio (response or error) finishes, always return to the idle state.
  // This gives control back to the user.
  audioPlayer.addEventListener("ended", () => {
    statusDisplay.textContent = "Click the mic to start.";
    updateButtonState("idle");
  });

  recordBtn.addEventListener("click", () => {
    if (currentState === "idle") {
      startRecording();
    } else if (currentState === "recording") {
      stopRecording();
    }
    // If 'processing', do nothing
  });

  // --- State Management Function ---
  function updateButtonState(newState) {
    currentState = newState;
    recordBtn.className = `record-btn ${newState}`;
    recordBtn.disabled = newState === "processing";

    micIcon.style.display = newState === "recording" ? "none" : "block";
    stopIcon.style.display = newState === "recording" ? "block" : "none";

    if (newState === "recording") {
      statusDisplay.textContent = "Listening...";
    } else if (newState === "processing") {
      statusDisplay.textContent = "Processing...";
    }
  }

  // --- Core Functions ---
  async function startRecording() {
    if (currentState !== "idle") return;

    if (!navigator.mediaDevices?.getUserMedia) {
      alert("Audio recording is not supported in this browser.");
      return;
    }

    updateButtonState("recording");
    audioPlayer.hidden = true;
    recordedChunks = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) recordedChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
        handleServerProcessing();
      };

      mediaRecorder.start();
    } catch (err) {
      console.error("Error accessing mic:", err);
      addMessageToChat(
        "System",
        "Could not access microphone.",
        "agent-message"
      );
      updateButtonState("idle");
    }
  }

  function stopRecording() {
    if (mediaRecorder && currentState === "recording") {
      mediaRecorder.stop();
      updateButtonState("processing");
    }
  }

  async function handleServerProcessing() {
    const blob = new Blob(recordedChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio_file", blob, "recording.webm");

    try {
      const response = await fetch(`/agent/chat/${sessionId}`, {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      if (response.ok) {
        addMessageToChat("You", result.user_query_text, "user-message");
        addMessageToChat("AI", result.llm_response_text, "agent-message");
        statusDisplay.textContent = "Here is my response:";
        playResponseAudio(result.audio_url);
      } else {
        handleApiError(result);
      }
    } catch (error) {
      handleApiError({ error: "Could not connect to the server." });
    }
  }

  function handleApiError(errorResult) {
    const errorMessage = errorResult.error || "An unknown error occurred.";
    addMessageToChat("System", errorMessage, "agent-message");

    if (errorResult.audio_url) {
      playResponseAudio(errorResult.audio_url);
    } else {
      statusDisplay.textContent = `Error: ${errorMessage}`;
      updateButtonState("idle");
    }
  }

  function playResponseAudio(url) {
    audioPlayer.src = url;
    // --- CHANGE: Keep the audio player hidden ---
    audioPlayer.hidden = true;
    audioPlayer.play();
  }

  function addMessageToChat(sender, message, className) {
    const p = document.createElement("p");
    p.className = className;
    p.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatHistoryDiv.appendChild(p);
    chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight;
  }

  // Set initial state
  updateButtonState("idle");
  statusDisplay.textContent = "Click the mic to start.";
});

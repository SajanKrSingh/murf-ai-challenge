document.addEventListener("DOMContentLoaded", () => {
  // --- UI Elements ---
  const startBtn = document.getElementById("startBtn");
  const stopBtn = document.getElementById("stopBtn");
  const audioPlayer = document.getElementById("audioPlayer");
  const statusDisplay = document.getElementById("statusDisplay");
  const recordingIndicator = document.getElementById("recordingIndicator");
  const sessionIdSpan = document.getElementById("sessionId");
  const chatHistoryDiv = document.getElementById("chatHistory");

  // --- State Variables ---
  let mediaRecorder;
  let recordedChunks = [];
  let sessionId;

  // --- Session Management ---
  // URL se session_id nikalna ya naya banana
  const urlParams = new URLSearchParams(window.location.search);
  sessionId = urlParams.get("session_id");
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    // URL ko update karna taki session ID save rahe
    window.history.replaceState({}, "", `?session_id=${sessionId}`);
  }
  // UI mein session ID ka chota version dikhana
  sessionIdSpan.textContent = `${sessionId.substring(0, 4)}...${sessionId.slice(
    -4
  )}`;

  // --- Event Listeners ---
  // Jab AI ka audio response khatam ho, toh agla recording shuru karo
  audioPlayer.addEventListener("ended", () => {
    // Sirf tabhi recording shuru karo jab पिछला audio ek successful response tha
    // aur buttons "Start Recording" ke state mein hain.
    if (!startBtn.disabled) {
      statusDisplay.textContent = "I'm listening...";
      startRecording();
    } else {
      // Error audio ke baad, user ko dobara try karne do
      statusDisplay.textContent = "Ready to try again.";
      startBtn.disabled = false;
    }
  });

  startBtn.addEventListener("click", startRecording);
  stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
    }
  });

  // --- Core Functions ---

  // Recording shuru karne ka function
  async function startRecording() {
    if (!navigator.mediaDevices?.getUserMedia) {
      alert("Audio recording is not supported in this browser.");
      return;
    }

    // Buttons aur UI elements ko update karna
    startBtn.disabled = true;
    stopBtn.disabled = false;
    recordingIndicator.hidden = false;
    audioPlayer.hidden = true;
    statusDisplay.textContent = ""; // Status ko recording indicator se replace karna
    recordedChunks = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) recordedChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop()); // Mic ko release karna
        handleStopRecording();
      };

      mediaRecorder.start();
    } catch (err) {
      console.error("Error accessing mic:", err);
      statusDisplay.textContent = "Could not access microphone.";
      startBtn.disabled = false;
      stopBtn.disabled = true;
      recordingIndicator.hidden = true;
    }
  }

  // Jab recording stop ho, toh is function ko call karna
  async function handleStopRecording() {
    recordingIndicator.hidden = true;
    statusDisplay.textContent = "Processing...";
    stopBtn.disabled = true;

    const blob = new Blob(recordedChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio_file", blob, "recording.webm");

    try {
      const response = await fetch(`/agent/chat/${sessionId}`, {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      // Response ko handle karna
      if (response.ok) {
        // Success Case
        addMessageToChat("You", result.user_query_text, "user-message");
        addMessageToChat("AI", result.llm_response_text, "agent-message");
        statusDisplay.textContent = "Here is my response:";
        playResponseAudio(result.audio_url);
      } else {
        // Error Case from Server
        handleApiError(result);
      }
    } catch (error) {
      // Network ya dusre client-side errors
      handleApiError({ error: "Could not connect to the server." });
    }
  }

  // Error handle karne ke liye ek hi function
  function handleApiError(errorResult) {
    const errorMessage = errorResult.error || "An unknown error occurred.";
    console.error("API Error:", errorMessage);
    statusDisplay.textContent = `Error: ${errorMessage}`;
    addMessageToChat("System", errorMessage, "agent-message");

    // Server se aayi hui error audio URL ko play karna
    if (errorResult.audio_url) {
      playResponseAudio(errorResult.audio_url);
    }

    // Error ke baad, start button ko re-enable karna
    startBtn.disabled = false;
  }

  // Audio play karne ka function
  function playResponseAudio(url) {
    audioPlayer.src = url;
    audioPlayer.hidden = false;
    audioPlayer.play();
  }

  // Chat history mein naya message add karne ka function
  function addMessageToChat(sender, message, className) {
    const p = document.createElement("p");
    p.className = className;

    const strong = document.createElement("strong");
    strong.textContent = sender;

    p.appendChild(strong);
    p.appendChild(document.createTextNode(`: ${message}`));

    chatHistoryDiv.appendChild(p);
    // Hamesha neeche scroll karna
    chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight;
  }
});

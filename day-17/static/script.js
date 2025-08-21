document.addEventListener("DOMContentLoaded", () => {
  // Aapke index.html ke according element IDs
  const recordBtn = document.getElementById("recordBtn");
  const statusDisplay = document.getElementById("statusDisplay");
  const audioPlayer = document.getElementById("audioPlayer");

  let mediaRecorder;
  let socket;
  let audioContext;
  let processor;
  let currentState = "idle";

  function setupWebSocket() {
    socket = new WebSocket("ws://127.0.0.1:8000/ws");
    socket.onopen = () => {
      console.log("WebSocket connection established.");
      statusDisplay.textContent = "Click the mic to start streaming.";
      updateButtonState("idle");
    };
    socket.onclose = () => {
      console.log("WebSocket connection closed.");
      statusDisplay.textContent = "Connection closed. Refresh to reconnect.";
      updateButtonState("idle");
      recordBtn.disabled = true;
    };
    socket.onerror = (error) => console.error("WebSocket Error:", error);
  }

  function updateButtonState(newState) {
    currentState = newState;
    // Aapke UI ke according button ki class change karna
    if (newState === "recording") {
      recordBtn.classList.add("recording");
      statusDisplay.textContent = "Streaming live...";
    } else {
      recordBtn.classList.remove("recording");
      statusDisplay.textContent = "Click the mic to start.";
    }
  }

  async function startRecording() {
    if (
      currentState !== "idle" ||
      !socket ||
      socket.readyState !== WebSocket.OPEN
    )
      return;

    updateButtonState("recording");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      audioContext = new (window.AudioContext || window.webkitAudioContext)({
        sampleRate: 16000, // AssemblyAI ke liye zaroori sample rate
      });

      const source = audioContext.createMediaStreamSource(stream);
      processor = audioContext.createScriptProcessor(1024, 1, 1);

      source.connect(processor);
      processor.connect(audioContext.destination);

      processor.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        const pcmData = new Int16Array(inputData.length);

        for (let i = 0; i < inputData.length; i++) {
          let s = Math.max(-1, Math.min(1, inputData[i]));
          pcmData[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
        }

        if (socket.readyState === WebSocket.OPEN) {
          socket.send(pcmData.buffer);
        }
      };

      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
    } catch (err) {
      console.error("Error accessing mic or setting up audio processing:", err);
      updateButtonState("idle");
    }
  }

  function stopRecording() {
    if (mediaRecorder && currentState === "recording") {
      mediaRecorder.stream.getTracks().forEach((track) => track.stop());
      if (audioContext) {
        audioContext.close();
      }
      if (socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
      updateButtonState("idle");
      statusDisplay.textContent = "Streaming stopped.";
    }
  }

  recordBtn.addEventListener("click", () => {
    if (currentState === "idle") {
      if (!socket || socket.readyState === WebSocket.CLOSED) {
        setupWebSocket();
        setTimeout(startRecording, 500);
      } else {
        startRecording();
      }
    } else if (currentState === "recording") {
      stopRecording();
    }
  });

  setupWebSocket();
});

const generateBtn = document.getElementById('generateBtn');
const textInput = document.getElementById('textInput');
const ttsPlayer = document.getElementById('ttsPlayer');

generateBtn.onclick = async () => {
    if (textInput.value.trim() === '') {
        alert('Please enter some text.');
        return;
    }
    const formData = new FormData();
    formData.append('text', textInput.value);
    try {
        const response = await fetch('/tts', { method: 'POST', body: formData });
        const data = await response.json();
        if (response.ok && data.audio_url) {
            ttsPlayer.src = data.audio_url;
            ttsPlayer.hidden = false;
            ttsPlayer.play();
        } else {
            alert('TTS generation failed.');
        }
    } catch (error) {
        alert('An error occurred.');
    }
};

// --- Echo Bot (Day 4 & 5) ---
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const echoPlayer = document.getElementById('echoPlayer');
const statusDiv = document.getElementById('status');

let mediaRecorder;
let audioChunks = [];

// Start Recording Function
startBtn.onclick = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        // --- onstop event handler (Day 5 Update) ---
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            echoPlayer.src = audioUrl;
            echoPlayer.hidden = false;
            
            // --- New Upload Logic for Day 5 ---
            statusDiv.textContent = '⬆️ Uploading recording...';
            const formData = new FormData();
            // Hum file ko 'recording.wav' naam se bhej rahe hain
            formData.append("audio_file", audioBlob, "recording.wav");

            try {
                const response = await fetch("/upload-audio", {
                    method: "POST",
                    body: formData,
                });
                const result = await response.json();

                if (response.ok) {
                    statusDiv.textContent = `✅ Upload complete! Size: ${result.size_bytes} bytes.`;
                } else {
                    statusDiv.textContent = `❌ Upload failed: ${result.error}`;
                }
            } catch (error) {
                console.error("Upload error:", error);
                statusDiv.textContent = '❌ Upload failed. Could not connect to server.';
            }
            // --- End of New Upload Logic ---

            audioChunks = [];
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        statusDiv.textContent = '🔴 Recording...';
        startBtn.disabled = true;
        stopBtn.disabled = false;
        echoPlayer.hidden = true;
        
    } catch (err) {
        statusDiv.textContent = 'Error: Could not access microphone.';
    }
};

// Stop Recording Function
stopBtn.onclick = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        statusDiv.textContent = '...Processing...';
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
};

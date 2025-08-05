
// --- Text to Speech (Day 2/3) ---
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
        const response = await fetch('/tts', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.audio_url) {
            ttsPlayer.src = data.audio_url;
            ttsPlayer.hidden = false;
            ttsPlayer.play();
        } else {
            console.error('TTS generation failed:', data);
            alert('TTS generation failed. Check the console for details.');
        }
    } catch (error) {
        console.error('Error calling TTS API:', error);
        alert('An error occurred. Could not connect to the server.');
    }
};


// --- Echo Bot (Day 4) ---
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const echoPlayer = document.getElementById('echoPlayer');
const statusDiv = document.getElementById('status');

let mediaRecorder;
let audioChunks = [];

// Start Recording Function
startBtn.onclick = async () => {
    try {
        // Get access to the microphone
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Initialize MediaRecorder
        mediaRecorder = new MediaRecorder(stream);
        
        // --- Event Handlers for MediaRecorder ---
        
        // 1. When data is available (i.e., a chunk of audio is recorded)
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        // 2. When recording is stopped
        mediaRecorder.onstop = () => {
            // Create a single audio blob from all the chunks
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            
            // Create a URL for the blob
            const audioUrl = URL.createObjectURL(audioBlob);
            
            // Set the URL to the audio player and make it visible
            echoPlayer.src = audioUrl;
            echoPlayer.hidden = false;
            
            // Clean up for the next recording
            audioChunks = [];
            
            // Stop all tracks on the stream to turn off the mic indicator
            stream.getTracks().forEach(track => track.stop());
        };
        
        // --- Start Recording and Update UI ---
        mediaRecorder.start();
        
        // Update UI elements
        statusDiv.textContent = '🔴 Recording...';
        startBtn.disabled = true;
        stopBtn.disabled = false;
        echoPlayer.hidden = true;
        
    } catch (err) {
        // Handle errors (e.g., user denies microphone permission)
        console.error("Error accessing microphone:", err);
        statusDiv.textContent = 'Error: Could not access microphone.';
        alert('Could not access the microphone. Please grant permission and try again.');
    }
};

// Stop Recording Function
stopBtn.onclick = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        
        // Update UI elements
        statusDiv.textContent = '✅ Recording stopped. Playing back...';
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
};

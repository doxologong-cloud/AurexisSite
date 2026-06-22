import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

phase3_js = """
// ==========================================
// PHASE 3: MEDIA & TERMINAL EASTER EGG
// ==========================================

// 1. Hacker Terminal Trigger
let keysPressed = '';
document.addEventListener('keydown', (e) => {
    // Only listen if not typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        if(e.target.id === 'hacker-input' && e.key === 'Enter') {
            handleHackerCommand(e.target.value);
            e.target.value = '';
        }
        return;
    }
    
    keysPressed += e.key.toLowerCase();
    if (keysPressed.length > 20) keysPressed = keysPressed.substring(1);
    
    if (keysPressed.includes('hacker')) {
        keysPressed = ''; // reset
        switchView('view-hacker');
        printHacker("AUREX OS ROOT ACCESS GRANTED.");
        printHacker("Type 'help' for commands.");
        setTimeout(() => document.getElementById('hacker-input').focus(), 100);
    }
});

function printHacker(text) {
    const out = document.getElementById('hacker-output');
    if (!out) return;
    out.innerHTML += `<div>> ${text}</div>`;
    out.parentElement.scrollTop = out.parentElement.scrollHeight;
}

function handleHackerCommand(cmd) {
    printHacker(cmd);
    const c = cmd.trim().toLowerCase();
    if (c === 'help') {
        printHacker("Commands: help, clear, ping, dox @user, matrix");
    } else if (c === 'clear') {
        document.getElementById('hacker-output').innerHTML = '';
    } else if (c === 'matrix') {
        printHacker("Initializing matrix protocol...");
        switchView('view-home');
        document.body.style.animation = 'glitch 0.2s infinite';
        setTimeout(() => document.body.style.animation = 'none', 2000);
    } else if (c.startsWith('dox ')) {
        const target = cmd.split(' ')[1];
        printHacker(`[+] Locating ${target}...`);
        setTimeout(() => printHacker(`[!] IP: 192.168.1.${Math.floor(Math.random()*255)}`), 1000);
        setTimeout(() => printHacker(`[!] Status: PWNED`), 2000);
    } else {
        printHacker("Command not found.");
    }
}

// 2. Voice Recording (MediaRecorder)
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

async function toggleVoiceRecord() {
    const btn = document.getElementById('btn-voice');
    if (!isRecording) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            isRecording = true;
            btn.style.color = '#ff4757';
            btn.style.animation = 'pulse 1s infinite alternate';
            
            mediaRecorder.ondataavailable = e => {
                audioChunks.push(e.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];
                // Simulate sending audio
                alert("Голосовое сообщение записано! (Интеграция с БД в след. фазе)");
                // Usually we'd upload to Supabase Storage and send the URL
            };
        } catch(e) {
            alert("Нет доступа к микрофону!");
        }
    } else {
        mediaRecorder.stop();
        isRecording = false;
        btn.style.color = 'var(--neon-color)';
        btn.style.animation = 'none';
        mediaRecorder.stream.getTracks().forEach(t => t.stop());
    }
}

// 3. Screen Capture (getDisplayMedia)
async function captureScreen() {
    try {
        const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
        const video = document.createElement('video');
        video.srcObject = stream;
        video.play();
        
        video.onloadedmetadata = () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            stream.getTracks().forEach(t => t.stop());
            
            const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
            // Simulate sending image
            alert("Скриншот сделан! (Интеграция с БД в след. фазе)");
        };
    } catch(e) {
        console.error("Окно захвата закрыто или отклонено.");
    }
}

// 4. Drag & Drop into Chat
const chatWindow = document.getElementById('chat-window');
if (chatWindow) {
    chatWindow.addEventListener('dragover', (e) => {
        e.preventDefault();
        chatWindow.style.border = '2px dashed var(--neon-color)';
    });
    chatWindow.addEventListener('dragleave', (e) => {
        e.preventDefault();
        chatWindow.style.border = 'none';
    });
    chatWindow.addEventListener('drop', (e) => {
        e.preventDefault();
        chatWindow.style.border = 'none';
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            alert(`Файл ${file.name} готов к отправке! (Загрузка в БД в след. фазе)`);
        }
    });
}
"""

if 'PHASE 3: MEDIA & TERMINAL EASTER EGG' not in js_text:
    js_text += "\n" + phase3_js
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js_text)
    print("Injected Phase 3 JS.")
else:
    print("Phase 3 JS already exists.")
